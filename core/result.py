from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Result:
    """
    The universal communication contract for all JARVIS subsystems.
    Every subsystem and plugin must return a Result object.
    """

    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[Exception] = None
    execution_time: float = 0.0  # Tracks structural processing time in ms