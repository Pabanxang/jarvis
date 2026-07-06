import platform
from datetime import datetime
from core.base_plugin import BasePlugin
from core.plugin_request import PluginRequest
from core.result import Result


class SystemInfoPlugin(BasePlugin):
    """Plugin capturing host operating system parameters and runtime details."""

    name = "sys_info"
    version = "1.0.0"
    description = "Exposes system environmental metrics, runtime versions, and wall-clock times."

    def execute(self, request: PluginRequest) -> Result:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        display_string = (
            f"JARVIS | Host OS: {platform.system()} ({platform.release()}) | "
            f"Python: {platform.python_version()} | Local Time: {now}"
        )
        return Result.success(display_string)