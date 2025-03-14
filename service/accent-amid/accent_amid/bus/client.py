# src/accent_amid/bus/client.py
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import aio_pika
from aio_pika.abc import AbstractExchange, AbstractRobustConnection

if TYPE_CHECKING:
    from collections.abc import Mapping

    from accent_amid.config import BusSettings

logger = logging.getLogger(__name__)


class BusClient:
    """Asynchronous client for interacting with a message bus (RabbitMQ).

    Uses aio-pika for asynchronous RabbitMQ communication.  Provides
    connection management and a simple interface for publishing messages.

    Attributes:
        _connection (AbstractRobustConnection | None): connection.
        _channel (aio_pika.Channel | None): channel.
        _exchange (AbstractExchange | None): exchange.
        _connected (bool): True if connected.

    """

    def __init__(self, settings: BusSettings) -> None:
        """Initialize BusClient.

        Args:
            settings (BusSettings): settings.

        """
        self._settings = settings
        self._connection: AbstractRobustConnection | None = None
        self._channel: aio_pika.Channel | None = None
        self._exchange: AbstractExchange | None = None
        self._connected = False

    async def connect(self) -> None:
        """Establish a connection to the message bus.

        Raises:
            Exception: If an error happens during connection.

        """
        if self._connected:
            return
        logger.info(
            "Connecting to RabbitMQ at %s:%s",
            self._settings.HOST,
            self._settings.PORT,
        )
        try:
            self._connection = await aio_pika.connect_robust(
                host=self._settings.HOST,
                port=self._settings.PORT,
                login=self._settings.USERNAME,
                password=self._settings.PASSWORD,
                virtualhost=self._settings.VHOST,
                timeout=self._settings.STARTUP_CONNECTION_DELAY,
            )
            self._channel = await self._connection.channel()
            self._exchange = await self._channel.declare_exchange(
                self._settings.EXCHANGE_NAME,
                type=self._settings.EXCHANGE_TYPE,
                durable=True,  # Consider making this configurable
            )
            self._connected = True
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.exception("Failed to connect to RabbitMQ: %s", e)
            raise

    async def close_connection(self) -> None:
        """Close the connection to the message bus.
        """
        if self._connected and self._connection:
            try:
                await self._connection.close()
                self._connected = False
                logger.info("RabbitMQ connection closed.")
            except Exception:
                logger.exception("Error closing RabbitMQ connection")

        self._connection = None  # Ensure connection is reset even on error
        self._channel = None
        self._exchange = None

    async def publish(self, event_name: str, headers: Mapping[str, Any]) -> None:
        """Publish a message to the message bus.

        Args:
            event_name (str): The name of the event.
            headers (Mapping[str, Any]): The headers to include in the message.

        Raises:
            Exception: connection.

        """
        if not self._connected:
            await self.connect()  # Auto-connect if not connected
            if (
                not self._connected
            ):  # Check again, after a potential failed connection attempt
                raise Exception("Cannot publish, not connected to bus.")

        message_body = b""  # Empty body, all data in headers

        message = aio_pika.Message(
            message_body,
            headers={"name": event_name, **headers},  # Include event_name
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Consider making configurable
        )

        if self._exchange is None:
            # Should not happen, due to connect and check.  Added to silence typing error.
            raise RuntimeError("Exchange is None.")
        await self._exchange.publish(
            message, routing_key=""
        )  # Headers exchange uses headers, not routing key

    async def __aenter__(self) -> BusClient:
        """Async context manager entry. Connects on entry.

        Returns:
             BusClient.

        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit. Closes connection on exit."""
        await self.close_connection()
