from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class PluginRequest:
    """Data container framing user intent and arguments for all JARVIS plugins."""
    query: str
    args: Dict[str, Any] = field(default_factory=dict)