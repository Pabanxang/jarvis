from __future__ import annotations

from typing import Optional

from core.logger import logger


class ApplicationContext:
    """
    Holds shared services and runtime state for JARVIS.
    """

    def __init__(self) -> None:
        self.logger = logger

        # Runtime services
        self.database: Optional[object] = None
        self.brain: Optional[object] = None
        self.skill_manager: Optional[object] = None

        # Runtime state
        self.running = False

    def initialize(self) -> None:
        self.logger.info("[CONTEXT] Initializing application context")
        self.running = True

    def shutdown(self) -> None:
        self.logger.info("[CONTEXT] Releasing application context")
        self.running = False