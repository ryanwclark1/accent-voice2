# accent_auth/purpose.py

import logging
from typing import Any

logger = logging.getLogger(__name__)


class Purpose:
    """Represents a user purpose (e.g., 'user', 'internal', 'external_api').

    Associates metadata plugins with each purpose to customize JWT data.
    """

    def __init__(self, name: str, metadata_plugins: list[Any] | None = None) -> None:
        """Initializes a Purpose instance.

        Args:
            name: The name of the purpose (e.g., 'user').
            metadata_plugins: A list of metadata plugin instances.
        """
        self.name: str = name
        self._metadata_plugins: list[Any] = (
            list(metadata_plugins) if metadata_plugins else []
        )

    @property
    def metadata_plugins(self) -> list[Any]:
        """Returns a copy of the list of metadata plugins."""
        return list(self._metadata_plugins)

    def add_metadata_plugin(self, metadata_plugin: Any) -> None:
        """Adds a metadata plugin to the purpose, if not already present."""
        if metadata_plugin not in self._metadata_plugins:
            self._metadata_plugins.append(metadata_plugin)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Purpose):
            return NotImplemented
        return (
            self.name == other.name
            and self._metadata_plugins == other._metadata_plugins
        )

    def __ne__(self, other: object) -> bool:
        return not self == other


class Purposes:
    """Manages a collection of Purpose instances."""

    valid_purposes = ["user", "internal", "external_api"]

    def __init__(
        self, purposes_config: dict[str, list[str]], metadata_plugins: dict[str, Any]
    ) -> None:
        """Initializes a Purposes instance.

        Args:
            purposes_config: A dictionary mapping purpose names to lists of
                plugin names.
            metadata_plugins: A dictionary mapping plugin names to plugin
                instances (loaded via stevedore).
        """
        self._metadata_plugins = metadata_plugins
        self._purposes: dict[str, Purpose] = {
            purpose: Purpose(purpose) for purpose in self.valid_purposes
        }
        self._set_default_user_purpose()
        self._set_default_internal_purpose()
        self._set_default_external_api_purpose()

        for purpose_name, plugin_names in purposes_config.items():
            purpose = self._purposes.get(purpose_name)
            if not purpose:
                logger.warning("Configuration has undefined purpose: %s", purpose_name)
                continue

            for plugin_name in plugin_names:
                plugin = self._get_metadata_plugin(plugin_name)
                if not plugin:
                    continue
                purpose.add_metadata_plugin(plugin.obj)  # Access .obj

    def _set_default_user_purpose(self) -> None:
        plugin = self._get_default_metadata_plugin("default_user")
        if not plugin:
            return
        self._purposes["user"].add_metadata_plugin(plugin.obj)  # Access .obj

    def _set_default_internal_purpose(self) -> None:
        plugin = self._get_default_metadata_plugin("default_internal")
        if not plugin:
            return
        self._purposes["internal"].add_metadata_plugin(plugin.obj)  # Access .obj

    def _set_default_external_api_purpose(self) -> None:
        plugin = self._get_default_metadata_plugin("default_external_api")
        if not plugin:
            return
        self._purposes["external_api"].add_metadata_plugin(plugin.obj)  # Access .obj

    def _get_default_metadata_plugin(self, plugin: str) -> Any | None:  # Changed to Any
        try:
            return self._metadata_plugins[plugin]
        except KeyError:
            logger.warning(
                "Purposes must have the following metadata plugins enabled: %s", plugin
            )
            return None  # Need to return None

    def _get_metadata_plugin(self, name: str) -> Any | None:  # Change to Any
        try:
            return self._metadata_plugins[name]
        except KeyError:
            logger.warning(
                "A purpose has been assigned to an invalid metadata plugin: %s", name
            )
            return None  # Need to return None

    def get(self, name: str) -> Purpose | None:
        """Retrieves a Purpose instance by name.

        Args:
            name: The name of the purpose.

        Returns:
            The Purpose instance, or None if not found.
        """
        return self._purposes.get(name)
