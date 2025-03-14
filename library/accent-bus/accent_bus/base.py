# core/base.py
import logging
from typing import Any, NamedTuple

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ConnectionParams(NamedTuple):
    """Connection parameters for RabbitMQ."""

    user: str
    password: str
    host: str
    port: int


class BaseProtocol:
    """Base class for publishers/consumers (to be extended by mixins)."""

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
    ): ...  # remove definition

    @property  # Correct.  This *is* a property.
    def url(self) -> str:
        """Returns the AMQP URL (must be implemented by subclasses)."""
        msg = "Subclasses must implement 'url'"
        raise NotImplementedError(msg)

    @property  # Correct. This *is* a property.
    def log(self) -> logging.Logger:
        """Returns the logger (must be implemented by subclasses)."""
        msg = "Subclasses must implement 'log'"
        raise NotImplementedError(msg)

class Base(BaseProtocol):
    """Base class for publishers/consumers (to be extended by mixins)."""

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
    ):
        self._name = name or type(self).__name__
        self._logger = logging.getLogger(type(self).__name__)
        self._connection_params = ConnectionParams(username, password, host, port)
        self._default_exchange_name = exchange_name
        self._default_exchange_type = exchange_type

    @property
    def url(self) -> str:
        """Constructs the RabbitMQ connection URL."""
        return (
            f"amqp://{self._connection_params.user}:{self._connection_params.password}@"
            f"{self._connection_params.host}:{self._connection_params.port}/"
        )

    @property
    def log(self) -> logging.Logger:
        """Returns the logger instance."""
        return self._logger


class RabbitMQConfig(BaseModel):
    """Configuration settings for RabbitMQ connection."""

    user: str = Field(default="guest", description="RabbitMQ username")
    password: str = Field(default="guest", description="RabbitMQ password")
    host: str = Field(default="localhost", description="RabbitMQ host")
    port: int = Field(default=5672, description="RabbitMQ port")
    exchange_name: str = Field(
        default="accent_bus_exchange", description="Default exchange name"
    )
    exchange_type: str = Field(default="topic", description="Default exchange type")

    @property
    def url(self) -> str:
        """Constructs the RabbitMQ connection URL."""
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"
