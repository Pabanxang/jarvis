from core.context import ApplicationContext
from core.result import Result

class Brain:
    """Stub implementation of Brain to support Assistant.py."""
    
    def __init__(self, context: ApplicationContext):
        self.context = context
        
    def process(self, command: str) -> Result:
        return Result(success=True, message=f"Brain received: {command}")
