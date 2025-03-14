# accent_bus/resources/common/abstract.py
# Copyright 2025 Accent Communications

"""Abstract event definitions."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Protocol

from .acl import escape as escape_acl
from .routing_key import escape as escape_key

if TYPE_CHECKING:
    from collections.abc import Mapping


class EventProtocol(Protocol):
    """Protocol for events."""

    __slots__ = ("content",)
    content: Mapping

    def __init__(self, content: Mapping | None = None) -> None:
        """Initialize an EventProtocol.

        Args:
           content (Mapping, optional): content

        """
        self.content = content or {}

    def __eq__(self, other: object) -> bool:
        """Equality comparison.

        Args:
          other: Another object to compare.

        Returns:
           bool: if two objects are equal

        """
        return (
            self.__class__ == other.__class__
            and self.content == other.content
            and vars(self) == vars(other)
        )

    def __ne__(self, other: object) -> bool:
        """Inequality comparison.

        Args:
            other: other object
        Returns:
            bool: if they are not equal

        """
        return not self == other

    def __repr__(self) -> str:
        """Return a representation of the event.

        Returns:
            str: String representation.

        """
        return self.__str__()

    def __str__(self) -> str:
        """Return a string representation of the event.

        Returns:
           str: String representation

        """
        return (
            f"<Event: {self.name} (headers: {self.headers}, content: {self.content})>"
        )

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the event name.

        Returns:
            str: event name

        """
        ...

    @property
    @abstractmethod
    def routing_key_fmt(self) -> str:
        """Return the routing key format string.

        Returns:
            str: routing key format

        """
        ...

    @property
    def routing_key(self) -> str:
        """Return the routing key.

        Returns:
            str: routing key

        """
        variables = dict(**self.content)
        variables.update(vars(self), name=self.name)
        variables = {
            key: escape_key(value) if isinstance(value, str) else value
            for key, value in variables.items()
        }
        return self.routing_key_fmt.format(**variables)

    @property
    def required_acl(self) -> str:
        """Return the required ACL string.

        **Deprecated**, use required_access instead

        Returns:
            str: required ACL

        """
        if hasattr(self, "required_acl_fmt"):
            variables = dict(**self.content)
            variables.update(vars(self), name=self.name)
            variables = {
                key: escape_acl(value) if isinstance(value, str) else value
                for key, value in variables.items()
            }
            return self.required_acl_fmt.format(**variables)
        return f"events.{self.routing_key}"

    @property
    # accent_bus/resources/common/abstract.py continued
    def required_access(self) -> str:
        """Return the required access string.

        Returns:
          str: required access

        """
        return f"event.{self.name}"

    @property
    def headers(self) -> dict:
        """Return the event headers.

        Returns:
           dict: event headers

        """
        headers = dict(vars(self))
        headers.update(name=self.name)
        return headers

    def marshal(self) -> dict:
        """Marshal the event content to a dictionary.

        Returns:
            dict: marshalled content.

        """
        return dict(self.content)


#  NOTE: Deprecated, use EventProtocol instead
class AbstractEvent(EventProtocol, metaclass=ABCMeta):
    """Abstract base class for events (deprecated)."""

    def __init__(self, content: dict | None = None) -> None:
        """Initialize AbstractEvent.

        Args:
          content (dict, optional): Content

        """
        self.content = content or {}
