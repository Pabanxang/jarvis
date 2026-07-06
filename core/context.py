from __future__ import annotations

from typing import Optional

from core.logger import logger
from core.plugin_manager import PluginManager


class ApplicationContext:
    """Holds shared runtime dependency services and resource state for JARVIS."""

    def __init__(self) -> None:
        self.logger = logger

        # Registered Systems
        self.database: Optional[object] = None
        self.brain: Optional[object] = None
        self.plugin_manager: Optional[PluginManager] = None

        self._initialized = False

    def initialize(self) -> None:
        if self._initialized:
            return

        self.logger.info("[CONTEXT] Initializing application context dependency registry")
        
        # Instantiate and inject our plugin orchestration engine
        self.plugin_manager = PluginManager(self)
        self._initialized = True

    def shutdown(self) -> None:
        self.logger.info("[CONTEXT] Releasing application context dependencies")
        if self.plugin_manager:
            self.plugin_manager.shutdown_all()
        self._initialized = False