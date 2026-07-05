from rich.console import Console
from rich.panel import Panel

from config import APP_NAME, VERSION
from core.logger import logger
from core.system import (
    check_internet,
    check_ollama,
    get_os,
    get_python,
)
from modules.fact.fact import get_fact

console = Console()


def startup():
    logger.info("[SYSTEM] Lifecycle | Jarvis Started")

    console.print(
        Panel.fit(
            f"[bold cyan]{APP_NAME}[/bold cyan]\nVersion {VERSION}",
            title="Starting",
        )
    )

    console.print()
    console.print(f"Operating System : {get_os()}")
    console.print(f"Python           : {get_python()}")

    # 1. Process Network Diagnostics
    internet = check_internet()
    if internet.success:
        console.print(f"[green]✓ Internet Connected[/green] ({internet.message})")
        logger.info(f"[NETWORK] Status: {internet.message}")
    else:
        console.print("[yellow]⚠ Offline Mode[/yellow]")
        logger.warning(f"[NETWORK] Status: {internet.message} | Error: {internet.error}")

    # 2. Process Local AI Engine Diagnostics
    ollama = check_ollama()
    if ollama.success:
        console.print(f"[green]✓ Ollama Running[/green] ({ollama.message})")
        logger.info(f"[OLLAMA] Status: {ollama.message}")
    else:
        console.print("[red]✗ Ollama Not Found[/red]")
        logger.error(f"[OLLAMA] Status: {ollama.message} | Error: {ollama.error}")

    # 3. Process Skill Layer Execution
    if internet.success:
        console.print()
        console.rule("Today's Fact")
        logger.info("[SKILL] Fact | Triggering network data fetch")
        console.print(f"\n{get_fact()}\n")
        logger.info("[SKILL] Fact | Render complete")

    console.print()
    console.print("[bold green]System Ready.[/bold green]")
    logger.info("[SYSTEM] Lifecycle | Startup complete. Engine Idle.")


if __name__ == "__main__":
    startup()