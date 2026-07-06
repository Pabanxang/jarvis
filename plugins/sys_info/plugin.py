import platform
from datetime import datetime
from core.base_plugin import BasePlugin
from core.event_bus import Event, EventBus
from core.plugin_request import PluginRequest
from core.result import Result


class SystemInfoPlugin(BasePlugin):
    """Concrete modular plugin capturing host operating system parameters and runtime details."""

    name = "sys_info"
    version = "1.0.0"
    description = "Exposes system environmental metrics, runtime versions, and wall-clock times."

    def initialize(self) -> Result:
        """Resolves the EventBus out of context and binds listener hooks (Option B)."""
        bus: EventBus = self.context.event_bus
        
        if bus:
            # Bind our internal callback loop to a targeted topic channel
            bus.subscribe("system.heartbeat", self.handle_heartbeat_event)
            self.context.logger.info(f"[{self.name.upper()}] Successfully bound to event stream: 'system.heartbeat'")
        
        return Result.success(f"Plugin '{self.name}' initialized cleanly.")

    def handle_heartbeat_event(self, event: Event) -> None:
        """Asynchronous style callback triggered purely when the event loop broadcasts."""
        sender = event.data.get("sender", "Unknown Source")
        self.context.logger.info(
            f"[{self.name.upper()} EVENT HOOK] Intercepted heartbeat from target '{sender}' at {event.timestamp}"
        )

    def execute(self, request: PluginRequest) -> Result:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        display_string = (
            f"JARVIS | Host OS: {platform.system()} ({platform.release()}) | "
            f"Python: {platform.python_version()} | Local Time: {now}"
        )
        return Result.success(display_string)