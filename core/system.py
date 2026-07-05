import platform
import socket
import time
import requests

from config import NETWORK_HOST, NETWORK_PORT, NETWORK_TIMEOUT, OLLAMA_API_URL
from core.result import Result


def check_internet() -> Result:
    """Validates real network connectivity against a public DNS using a high-res clock."""
    start_time = time.perf_counter()

    try:
        socket.create_connection((NETWORK_HOST, NETWORK_PORT), timeout=NETWORK_TIMEOUT)
        execution_time = (time.perf_counter() - start_time) * 1000
        return Result(
            success=True,
            message=f"Connected ({int(execution_time)}ms)",
            data={"latency_ms": int(execution_time)},
            duration_ms=round(execution_time, 2),
        )
    except OSError as e:
        execution_time = (time.perf_counter() - start_time) * 1000
        return Result(
            success=False,
            message=f"Connection failed: {e}",
            error=e,
            duration_ms=round(execution_time, 2),
        )


def check_ollama() -> Result:
    """Validates that the local Ollama backend engine is awake, running, and responsive."""
    start_time = time.perf_counter()

    try:
        # Pings the actual running local server port directly
        response = requests.get(OLLAMA_API_URL, timeout=NETWORK_TIMEOUT)
        execution_time = (time.perf_counter() - start_time) * 1000
        
        if response.status_code == 200:
            return Result(
                success=True,
                message="Daemon Active (API Status: 200 OK)",
                duration_ms=round(execution_time, 2),
            )
        else:
            return Result(
                success=False,
                message=f"Daemon Unhealthy (API Status: {response.status_code})",
                duration_ms=round(execution_time, 2),
            )
    except requests.RequestException as e:
        execution_time = (time.perf_counter() - start_time) * 1000
        return Result(
            success=False,
            message=f"Daemon Stopped or Offline: {e}",
            error=e,
            duration_ms=round(execution_time, 2),
        )


def get_os() -> str:
    return platform.system()


def get_python() -> str:
    return platform.python_version()