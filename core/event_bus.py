from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List


@dataclass(frozen=True)
class Event:
    """An immutable, structured message payload emitted over the application framework space."""
    topic: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class EventBus:
    """Centralized synchronous message broker managing lightweight subscription routing maps."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}

    def subscribe(self, topic: str, callback: Callable[[Event], None]) -> None:
        """Attaches an observer callable closure to listen for specific broadcast channels."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    def publish(self, topic: str, data: Dict[str, Any]) -> None:
        """Broadcasts an immutable event packet down to all registered callback observers."""
        if topic not in self._subscribers:
            return

        event_packet = Event(topic=topic, data=data)
        for callback in self._subscribers[topic]:
            try:
                callback(event_packet)
            except Exception as e:
                # Keep event propagation fault-tolerant so broken consumers don't tank the bus
                print(f"[EVENT BUS ERROR] Subscriber crash on topic '{topic}': {str(e)}")