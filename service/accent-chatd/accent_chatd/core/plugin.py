# src/accent_chatd/core/plugin.py

from abc import ABC, abstractmethod
from typing import Any


class Plugin(ABC):
    """Abstract base class for plugins.

    All plugins should inherit from this class and implement the `load` method.
    """

    @abstractmethod
    def load(self, dependencies: dict[str, Any]) -> None:
        """Loads the plugin, registering any necessary components with the application.

        Args:
            dependencies: A dictionary of dependencies that the plugin can use.
                            This will typically include the FastAPI app instance,
                            configuration settings, database access, etc.

        """
