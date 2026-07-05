import platform
import socket
import subprocess
import time

from core.result import Result


def check_internet() -> Result:
    """Validates network connectivity against Google's public DNS."""
    host = "8.8.8.8"
    port = 53
    timeout = 3
    start_time = time.time()

    try:
        socket.create_connection((host, port), timeout=timeout)
        latency = int((time.time() - start_time) * 1000)
        return Result(
            success=True,
            message=f"Connected ({latency}ms)",
            data={"latency_ms": latency},
        )
    except OSError as e:
        return Result(success=False, message="Offline", error=e)


def check_ollama() -> Result:
    """Validates that the local Ollama daemon is active and running."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=3,
        )
        version_string = result.stdout.strip()
        return Result(
            success=True,
            message=f"Running ({version_string})",
            data={"version": version_string},
        )
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        return Result(success=False, message="Not Found", error=e)


def get_os() -> str:
    return platform.system()


def get_python() -> str:
    return platform.python_version()