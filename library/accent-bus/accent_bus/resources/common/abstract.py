# resources/common/abstract.py
import logging
from typing import Any, ClassVar, NamedTuple

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)


class ConnectionParams(NamedTuple):
    """Connection parameters for RabbitMQ."""

    user: str
    password: str
    host: str
    port: int


class BaseProtocol:
    """Base protocol for publishers and consumers."""

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
    ): ...  # Remove definition

    @property
    def url(self) -> str: ...  # Remove definition

    @property
    def log(self) -> logging.Logger: ...  # remove definition


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


# --- Event Protocol ---
class EventProtocol(BaseModel):
    """Protocol definition for events.

    Ensures all events have necessary properties and methods.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # Needed for ClassVar, routing and acl.

    content: dict
    name: ClassVar[str]
    routing_key_fmt: ClassVar[str]
    required_acl_fmt: ClassVar[str]

    @property
    def routing_key(self) -> str:
        """Calculates the routing key for the event.

        Returns:
            str: The routing key.

        """

    @property
    def required_access(self) -> str:
        """Defines the required access level for the event.

        Returns:
            str:  access level.

        """

    @property
    def headers(self) -> dict:
        """Generates headers for the event message.

        Returns:
            dict: A dictionary of headers.

        """
        headers = dict(vars(self))  # instance attributes
        headers["name"] = self.name  # Add the event name
        return headers

    def marshal(self) -> dict:
        """Marshals the event data into a dictionary.

        Returns:
             dict: The event data.

        """
        return self.model_dump()  # Use Pydantic's model_dump
