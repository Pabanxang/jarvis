from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.plugin_request import PluginRequest
from core.result import Result

if TYPE_CHECKING:
    from core.context import ApplicationContext


class BasePlugin(ABC):
    """Abstract baseline class establishing lifecycle hooks and execution contracts for all plugins."""

    name: str = "Unknown"
    version: str = "0.0"
    description: str = ""

    def __init__(self, context: ApplicationContext) -> None:
        self.context = context

    def initialize(self) -> Result:
        """Invoked when the plugin is discovered and mounted into runtime memory."""
        return Result.success(f"Plugin '{self.name}' initialized cleanly.")

    @abstractmethod
    def execute(self, request: PluginRequest) -> Result:
        """Primary functional runtime entry point handling execution logic."""
        pass

    def shutdown(self) -> Result:
        """Invoked during system teardown to guarantee safe resource isolation."""
        return Result.success(f"Plugin '{self.name}' safely unloaded.")