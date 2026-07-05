from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Result:
    """The universal communication contract for all JARVIS subsystems."""

    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[Exception] = None
    duration_ms: float = 0.0  # Tracks structural processing time