from core.base_plugin import BasePlugin
from core.plugin_request import PluginRequest
from core.result import Result


class FactPlugin(BasePlugin):
    """Concrete modular plugin delivering structural architectural insights and computing history."""

    name = "fact"
    version = "1.0.0"
    description = "Provides historical insights and system trivia."

    def execute(self, request: PluginRequest) -> Result:
        query_text = request.query.lower()

        # Handle architectural context or fall back to computing history
        if "architecture" in query_text:
            fact_payload = (
                "The historic Nyatapola Temple of Bhaktapur, completed in 1702, features five distinct structural tiers "
                "with perfectly balanced geometry that allowed it to survive both major Nepalese earthquakes in 1934 and 2015."
                " It remains a masterclass in structural wooden engineering."
            )
        else:
            fact_payload = (
                "The computer bug got its name when legendary computer scientist Grace Hopper found an actual "
                "moth trapped inside a relay of the Harvard Mark II computer in 1947."
            )

        return Result.success(fact_payload)