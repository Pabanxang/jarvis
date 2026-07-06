from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class PluginRequest:
    """An immutable data container framing user intent and arguments for all JARVIS plugins."""
    query: str
    args: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Enforce clean string stripping upon instantiation
        object.__setattr__(self, "query", self.query.strip())