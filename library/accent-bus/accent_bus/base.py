# base.py
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
    """Base protocol for publishers and consumers.
    Implements shared properties and abstract methods.
    """

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
    ):
        """Initializes the BaseProtocol.

        Args:
            name (str | None): The name of the component.
            username (str, optional): RabbitMQ username. Defaults to "guest".
            password (str, optional): RabbitMQ password. Defaults to "guest".
            host (str, optional): RabbitMQ host. Defaults to "localhost".
            port (int, optional): RabbitMQ port. Defaults to 5672.
            exchange_name (str, optional):  Name of the exchange.
            exchange_type (str, optional):  Type of exchange (topic, direct, etc)
            **kwargs: Additional keyword arguments.

        """

    @property
    def url(self) -> str:
        """Returns the AMQP URL.

        Returns:
            str: The AMQP URL.

        """

    @property
    def log(self) -> logging.Logger:
        """Returns the logger instance.

        Returns:
            logging.Logger: The logger.

        """


class Base(BaseProtocol):
    """Base class for publishers/consumers (to be extended by mixins).

    Args:
        name (str | None): The name of the component.
        username (str, optional): RabbitMQ username. Defaults to "guest".
        password (str, optional): RabbitMQ password. Defaults to "guest".
        host (str, optional): RabbitMQ host. Defaults to "localhost".
        port (int, optional): RabbitMQ port. Defaults to 5672.
        exchange_name (str, optional): Name of the exchange.
        exchange_type (str, optional): Type of exchange.
        **kwargs: Additional keyword arguments.

    """

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
        """Constructs the RabbitMQ connection URL.

        Returns:
            str: The complete AMQP URL.

        """
        return (
            f"amqp://{self._connection_params.user}:{self._connection_params.password}@"
            f"{self._connection_params.host}:{self._connection_params.port}/"
        )

    @property
    def log(self) -> logging.Logger:
        """Returns the logger instance.

        Returns:
            logging.Logger: The logger instance.

        """
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
        """Constructs the RabbitMQ connection URL.

        Returns:
            str: The complete AMQP URL.

        """
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"
