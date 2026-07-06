# plugins/fact/fact_plugin.py
from core.base_plugin import BasePlugin
from core.plugin_request import PluginRequest
from core.result import Result

class FactPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "fact"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Random facts"

    def initialize(self) -> Result:
        return Result.ok(f"Plugin '{self.name}' built successfully.")

    def execute(self, request: PluginRequest) -> Result:
        return Result.ok("The historic Nyatapola Temple of Bhaktapur, completed in 1702, features five distinct structural tiers.")