import importlib
import os
import pkgutil
from typing import Dict, Type

from core.base_plugin import BasePlugin
from core.context import ApplicationContext
from core.plugin_request import PluginRequest
from core.result import Result


class PluginManager:
    """Handles the lifecycle, dynamic auto-discovery, and routing of plugins."""

    def __init__(self, context: ApplicationContext) -> None:
        self.context = context
        self.plugins: Dict[str, BasePlugin] = {}
        self._plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "plugins"))

    def discover_and_load(self) -> None:
        """Crawls the plugins/ directory and loads compatible BasePlugin modules dynamically."""
        if not os.path.exists(self._plugins_dir):
            self.context.logger.warning(f"[PLUGINS] Directory not found at: {self._plugins_dir}")
            return

        self.context.logger.info("[PLUGINS] Beginning dynamic plugin discovery loop...")

        # Walk through subdirectories inside the plugins/ folder
        for _, name, ispkg in pkgutil.iter_modules([self._plugins_dir]):
            if ispkg:
                try:
                    # Dynamically import the plugin package module
                    module_name = f"plugins.{name}.{name}_plugin"
                    module = importlib.import_module(module_name)

                    # Inspect modules for attributes that subclass BasePlugin
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, BasePlugin)
                            and attr is not BasePlugin
                        ):
                            # Instantiate with our context injected safely
                            plugin_instance = attr(self.context)
                            
                            # Run internal init check
                            init_result = plugin_instance.initialize()
                            if init_result.is_ok:
                                self.plugins[plugin_instance.name] = plugin_instance
                                self.context.logger.info(
                                    f"[PLUGINS] Successfully loaded: {plugin_instance.name} [v{plugin_instance.version}]"
                                )
                            else:
                                self.context.logger.error(
                                    f"[PLUGINS] Failed to initialize plugin {plugin_instance.name}: {init_result.error_message}"
                                )

                except Exception as e:
                    self.context.logger.error(f"[PLUGINS] Error auto-discovering plugin '{name}': {str(e)}")

        self.context.logger.info(f"[PLUGINS] Finished discovery. Total active plugins loaded: {len(self.plugins)}")

    def route_request(self, target_plugin_name: str, request: PluginRequest) -> Result:
        """Safely dispatches an isolated PluginRequest envelope to an active plugin."""
        plugin = self.plugins.get(target_plugin_name)
        if not plugin:
            return Result.fail(f"Execution failed: Target plugin '{target_plugin_name}' is not loaded or active.")

        try:
            self.context.logger.info(f"[PLUGINS] Routing request to plugin: '{target_plugin_name}'")
            return plugin.execute(request)
        except Exception as e:
            return Result.fail(f"Unhandled runtime exception inside plugin '{target_plugin_name}': {str(e)}")

    def shutdown_all(self) -> None:
        """Gracefully unloads and releases resources for all active plugins."""
        for name, plugin in list(self.plugins.items()):
            shutdown_result = plugin.shutdown()
            if shutdown_result.is_ok:
                self.context.logger.info(f"[PLUGINS] Gracefully unloaded: {name}")
            self.plugins.pop(name)