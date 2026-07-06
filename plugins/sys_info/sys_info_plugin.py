# plugins/sys_info/sys_info_plugin.py
import platform
from datetime import datetime
from core.base_plugin import BasePlugin
from core.plugin_request import PluginRequest
from core.result import Result

class SystemInfoPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "sys_info"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Exposes system environmental metrics"

    def initialize(self) -> Result:
        bus = self.context.event_bus
        if bus:
            bus.subscribe("system.heartbeat", self.handle_heartbeat_event)
        return Result.ok(f"Plugin '{self.name}' initialized cleanly.")

    def handle_heartbeat_event(self, event) -> None:
        self.context.logger.info(f"[SYS_INFO EVENT HOOK] Intercepted heartbeat")

    def execute(self, request: PluginRequest) -> Result:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        display_string = f"JARVIS | Host OS: {platform.system()} | Local Time: {now}"
        return Result.ok(display_string)