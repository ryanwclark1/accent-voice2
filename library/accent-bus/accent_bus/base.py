# accent_bus/base.py
# Copyright 2025 Accent Communications

"""Base classes for AMQP consumers and publishers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, NamedTuple, Protocol, Self

if TYPE_CHECKING:
    from types import TracebackType


class ConnectionParams(NamedTuple):
    """Connection parameters for AMQP."""

    user: str
    password: str
    host: str
    port: int


class EventProtocol(Protocol):
    """Protocol for events."""

    name: str
    content: dict

    def is_valid(self) -> bool:
        """Check if the event is valid."""
        ...

    def marshal(self) -> dict:
        """Marshal the event to a dictionary."""
        ...

    @property
    def routing_key(self) -> str:
        """Return the routing key for the event."""
        ...

    @property
    def headers(self) -> dict:
        """Return the headers for the event."""
        ...


class BaseProtocol(Protocol):
    """Base protocol for AMQP consumers and publishers."""

    _name: str
    _logger: logging.Logger
    _connection_params: ConnectionParams
    _default_exchange_name: str
    _default_exchange_type: str

    def __init__(
        self,
        name: str | None,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672,
        exchange_name: str = "",
        exchange_type: str = "",
        **kwargs: Any,
    ) -> None: ...

    @property
    def url(self) -> str:
        """Return the AMQP URL."""
        ...

    @property
    def log(self) -> logging.Logger:
        """Return the logger."""
        ...

    @property
    async def is_running(self) -> bool:
        """Check if the consumer/publisher is running."""
        ...

    def _marshal(
        self,
        event: EventProtocol,  # Use the correct EventProtocol
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict | None, dict | None, str | None]:
        """Marshal an event into headers, payload, and routing key."""
        ...

    def _unmarshal(
        self, event_name: str, headers: dict, payload: dict
    ) -> tuple[dict, dict]:
        """Unmarshal headers and payload into a dictionary."""
        ...

    async def __aenter__(self) -> Self:
        """Enter the context."""
        ...

    async def __aexit__(
        self,
        exc: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,  # Corrected variable name
    ) -> None:
        """Exit the context."""
        ...


class Base(BaseProtocol):
    """Base class for publishers/consumers (to be extended by mixins)."""

    def __init__(
        self,
        name: str | None = None,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672,
        exchange_name: str = "",
        exchange_type: str = "",
        **kwargs: Any,
    ) -> None:
        """Initialize the Base class.

        Args:
            name (str, optional): The name of the consumer/publisher.
                Defaults to class name.
            username (str, optional): The username for AMQP connection.
                Defaults to 'guest'.
            password (str, optional): The password for AMQP connection.
                Defaults to 'guest'.
            host (str, optional): The AMQP host. Defaults to 'localhost'.
            port (int, optional): The AMQP port. Defaults to 5672.
            exchange_name (str, optional): The default exchange name.
                Defaults to ''.
            exchange_type (str, optional): The default exchange type.
                Defaults to ''.
            **kwargs: Additional keyword arguments.

        """
        self._name = name or type(self).__name__
        self._logger = logging.getLogger(type(self).__name__)
        self._connection_params = ConnectionParams(username, password, host, port)
        self._default_exchange_name = exchange_name
        self._default_exchange_type = exchange_type

    @property
    def url(self) -> str:
        """Return the AMQP URL.

        Returns:
            str: The AMQP URL.

        """
        return (
            f"amqp://{self._connection_params.user}:{self._connection_params.password}@"
            f"{self._connection_params.host}:{self._connection_params.port}/"
        )

    @property
    def log(self) -> logging.Logger:
        """Return the logger.

        Returns:
           logging.Logger: The logger instance.

        """
        return self._logger

    @property
    async def is_running(self) -> bool:
        """Check if running.  Placeholder for more specific checks in subclasses.

        Returns:
             bool: Always returns True.

        """
        return True

    def _marshal(
        self,
        event: EventProtocol,
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict | None, dict | None, str | None]:
        """Marshal an event into headers, payload, and routing key.

        Args:
            event (EventProtocol): The event to marshal.
            headers (dict | None): Optional headers.
            payload (dict | None): Optional payload.
            routing_key (str | None): Optional routing key.

        Returns:
            tuple[dict | None, dict | None, str | None]: The marshaled headers,
                payload, and routing key.

        """
        return headers, payload, routing_key

    def _unmarshal(
        self, event_name: str, headers: dict, payload: dict
    ) -> tuple[dict, dict]:
        """Unmarshal headers and payload.

        Args:
            event_name (str): The name of the event.
            headers (dict): The headers.
            payload (dict): The payload.

        Returns:
            tuple[dict, dict]: The unmarshaled headers and payload.

        """
        return headers, payload

    async def __aenter__(self) -> Self:
        """Asynchronous context manager entry.

        Returns:
            Self: Returns self.

        """
        return self

    async def __aexit__(
        self,
        exc: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Asynchronous context manager exit.

        Args:
            exc (type[BaseException] | None): Exception type.
            exc_value (BaseException | None): Exception value.
            traceback (TracebackType | None): Traceback object.

        """
