# accent_bus/collectd/common.py
# Copyright 2025 Accent Communications

"""Common Collectd event definitions."""

from __future__ import annotations

from abc import abstractmethod

from accent_bus.resources.common.abstract import EventProtocol


class CollectdEvent(EventProtocol):
    """Base Collectd Event.

    Subclasses must define the following attributes:
      * name
      * routing_key_fmt
      * plugin
      * type_
    """

    routing_key_fmt: str
    interval: int = 10
    plugin_instance: str | None = None
    time: str | int = "N"
    type_instance: str | None = None
    values: tuple[str, ...] = ()

    def __init__(self, content: dict | None = None) -> None:
        """Initialize a CollectdEvent.

        Args:
            content (dict, optional): The event content. Defaults to {}.

        """
        self.content = content or {}

    @property
    @abstractmethod
    def plugin(self) -> str:
        """Return the plugin name.

        Returns:
            str: plugin name

        """

    @property
    @abstractmethod
    def type_(self) -> str:
        """Return the type.

        Returns:
           str: type

        """

    def is_valid(self) -> bool:
        """Check if the event is valid.

        Returns:
           bool: if the event is valid

        """
        return (
            self.plugin is not None
            and self.plugin_instance is not None
            and self.type_ is not None
            and self.type_instance is not None
            and (self.time == "N" or isinstance(self.time, int))
            and len(self.values) > 0
        )

    def __str__(self) -> str:
        """Return a string representation of the event.

        Returns:
           str: String representation.

        """
        content = ", ".join(
            [
                f"plugin='{self.plugin}'",
                f"plugin_instance='{self.plugin_instance}'",
                f"type='{self.type_}'",
                f"type_instance='{self.type_instance}'",
                f"values={self.values}",
            ]
        )
        return f"CollectdEvent({content})"
