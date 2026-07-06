# core/brain.py
from __future__ import annotations
from typing import TYPE_CHECKING, Dict

from core.plugin_request import PluginRequest
from core.result import Result

if TYPE_CHECKING:
    from core.context import ApplicationContext


class Brain:
    """The central processing core responsible for command token parsing and route dispatching."""

    def __init__(self, context: ApplicationContext) -> None:
        self.context = context
        self._memory: Dict[str, str] = {}

    def process_input(self, raw_input: str) -> Result:
        cleaned_input = raw_input.strip()
        if not cleaned_input:
            return Result.fail("Input is completely empty.")

        tokens = cleaned_input.split(" ", 1)
        command = tokens[0].lower()
        payload = tokens[1].strip() if len(tokens) > 1 else ""

        if command == "help":
            return self._handle_help()
        elif command == "plugins":
            return self._handle_plugins_list()
        elif command in ("remember", "forget", "recall"):
            return self._handle_memory(command, payload)
        elif command in ("fact", "time", "system"):
            return self._dispatch_to_plugin(command, payload)
        else:
            return Result.fail(
                f"Unknown command instruction '{command}'. Type 'help' to view active directives."
            )

    def _handle_help(self) -> Result:
        help_text = (
            "\n=== JARVIS Core Command Directives ===\n"
            "• help                - Displays this operational command registry menu.\n"
            "• plugins             - Inspects and lists all auto-discovered runtime modules.\n"
            "• fact [query]        - Routes to the Fact system extension.\n"
            "• system / time       - Routes to the System Info extension to capture host metrics.\n"
            "• remember [key] [val]- Stashes an architectural note or variable into runtime memory.\n"
            "• recall [key]        - Recovers a stashed value from runtime memory.\n"
            "• forget [key]        - Expunges a targeted key out of runtime memory."
        )
        return Result.ok(help_text)

    def _handle_plugins_list(self) -> Result:
        manager = self.context.plugin_manager
        if not manager or not manager.plugins:
            return Result.ok("Active plugin registry is currently empty.")

        lines = ["\n=== Active Discovered Plugins ==="]
        for name, instance in manager.plugins.items():
            lines.append(f"• [{name.upper()}] v{getattr(instance, 'version', '1.0')} - {getattr(instance, 'description', '')}")
        return Result.ok("\n".join(lines))

    def _handle_memory(self, action: str, payload: str) -> Result:
        if action == "remember":
            if not payload or " " not in payload:
                return Result.fail("Usage error. Design format: remember [key] [your information content]")
            key, val = payload.split(" ", 1)
            self._memory[key.lower()] = val.strip()
            return Result.ok(f"Stored reference for '{key}' successfully into runtime memory.")

        elif action == "recall":
            if not payload:
                return Result.fail("Usage error. Design format: recall [key]")
            val = self._memory.get(payload.lower())
            if not val:
                return Result.fail(f"No active record found matching key reference '{payload}'.")
            return Result.ok(f"Recalled [{payload}]: {val}")

        elif action == "forget":
            if not payload:
                return Result.fail("Usage error. Design format: forget [key]")
            if payload.lower() in self._memory:
                self._memory.pop(payload.lower())
                return Result.ok(f"Expunged key reference '{payload}' from active environment maps.")
            return Result.fail(f"No records found matching key reference '{payload}'.")

        return Result.fail("Invalid structural path passing inside memory subsystems.")

    def _dispatch_to_plugin(self, command: str, payload: str) -> Result:
        manager = self.context.plugin_manager
        if not manager:
            return Result.fail("The internal framework PluginManager layer is currently offline.")

        target_plugin = "sys_info" if command in ("time", "system") else "fact"
        request_envelope = PluginRequest(query=payload)
        return manager.route_request(target_plugin, request_envelope)