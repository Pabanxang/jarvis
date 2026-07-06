# core/base_plugin.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.context import ApplicationContext
    from core.plugin_request import PluginRequest
    from core.result import Result

class BasePlugin(ABC):
    """Abstract structural baseline for all auto-discovered modular extensions."""

    def __init__(self, context: ApplicationContext) -> None:
        self.context = context

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    def initialize(self) -> Result:
        from core.result import Result
        # CHANGED: Swapped Result.success -> Result.ok to match your core class implementation
        return Result.ok(f"Plugin {self.name} initialized.")

    @abstractmethod
    def execute(self, request: PluginRequest) -> Result:
        pass

    def shutdown(self) -> Result:
        from core.result import Result
        # CHANGED: Swapped Result.success -> Result.ok to match your core class implementation
        return Result.ok(f"Plugin {self.name} shut down cleanly.")