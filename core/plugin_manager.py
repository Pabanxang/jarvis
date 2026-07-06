# core/context.py
from core.event_bus import EventBus
from core.plugin_manager import PluginManager
from core.logger import logger  # Ensure this matches your logging utility path

class ApplicationContext:
    """Holds shared runtime dependency services and resource state for JARVIS."""

    def __init__(self) -> None:
        self.logger = logger
        self.event_bus = None
        self.plugin_manager = None
        self._initialized = False

    def initialize(self) -> None:
        if self._initialized:
            return

        self.logger.info("[CONTEXT] Initializing core application framework context...")
        
        # 1. Mount event line
        self.event_bus = EventBus()
        
        # 2. Mount plugin processing core
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.discover_and_load()
        
        self._initialized = True
        self.logger.info("[CONTEXT] System core dependencies mounted successfully.")

    def shutdown(self) -> None:
        self.logger.info("[CONTEXT] Commencing core system teardown...")
        if self.plugin_manager:
            self.plugin_manager.shutdown_all()
        self._initialized = False