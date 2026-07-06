from __future__ import annotations

from typing import Optional

from core.event_bus import EventBus
from core.logger import logger
from core.plugin_manager import PluginManager


class ApplicationContext:
    """Holds shared runtime dependency services and resource state for JARVIS."""

    def __init__(self) -> None:
        self.logger = logger
        self.event_bus: Optional[EventBus] = None
        self.plugin_manager: Optional[PluginManager] = None
        self._initialized = False

    def initialize(self) -> None:
        if self._initialized:
            return

        self.logger.info("[CONTEXT] Initializing core application framework context...")
        
        # 1. Spin up the Event Bus first so other components can bind to it immediately
        self.event_bus = EventBus()
        
        # 2. Spin up the Plugin Manager and pass our context downwards
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.discover_and_load()
        
        self._initialized = True
        self.logger.info("[CONTEXT] System core dependencies mounted successfully.")

    def shutdown(self) -> None:
        self.logger.info("[CONTEXT] Commencing core system teardown...")
        if self.plugin_manager:
            self.plugin_manager.shutdown_all()
        self._initialized = False