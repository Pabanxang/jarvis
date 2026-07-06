import platform
import socket
import time
import requests
from functools import wraps

from config import NETWORK_HOST, NETWORK_PORT, NETWORK_TIMEOUT, OLLAMA_API_URL
from core.result import Result


def measure_execution(func):
    """Decorator to measure execution time and catch unhandled exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Result:
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = Result(success=False, message=str(e), error=e)
            
        execution_time = (time.perf_counter() - start_time) * 1000
        result.execution_time = round(execution_time, 2)
        return result
    return wrapper


@measure_execution
def check_internet() -> Result:
    """Validates real network connectivity against a public DNS."""
    with socket.create_connection((NETWORK_HOST, NETWORK_PORT), timeout=NETWORK_TIMEOUT):
        pass
    return Result(success=True, message="Connected")


@measure_execution
def check_ollama() -> Result:
    """Validates that the local Ollama backend engine is awake and responsive."""
    response = requests.get(OLLAMA_API_URL, timeout=NETWORK_TIMEOUT)
    if response.status_code == 200:
        return Result(success=True, message="Daemon Active (API Status: 200 OK)")
    return Result(success=False, message=f"Daemon Unhealthy (API Status: {response.status_code})")


def get_os() -> str:
    return platform.system()


def get_python() -> str:
    return platform.python_version()