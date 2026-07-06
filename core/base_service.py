from abc import ABC
from core.context import ApplicationContext


class BaseService(ABC):
    """Universal abstract base class for all background service components in JARVIS."""

    def __init__(self, context: ApplicationContext):
        self.context = context

    def initialize(self) -> None:
        """Executed when the service is registered and mounted by the container loop."""
        pass

    def shutdown(self) -> None:
        """Executed during system teardown to guarantee graceful resource isolation."""
        pass