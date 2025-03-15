# src/accent_chatd/core/bus.py
import asyncio
import json
import logging
from collections.abc import Callable, Coroutine
from typing import Any

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from accent_chatd.core.config import get_settings

logger = logging.getLogger(__name__)


class BusPublisher:
    def __init__(self, connection_url: str, exchange_name: str):
        self._connection_url = connection_url
        self._exchange_name = exchange_name
        self._connection = None
        self._channel = None
        self._exchange = None

    async def _connect(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self._connection_url)
            self._channel = await self._connection.channel()
            self._exchange = await self._channel.declare_exchange(
                self._exchange_name, type=aio_pika.ExchangeType.HEADERS, durable=True
            )  # Ensure exchange is durable

    async def publish(
        self, message: Any, routing_key: str = "", headers: dict | None = None
    ):
        """Publishes a message to the configured exchange."""
        await self._connect()
        body = json.dumps(message).encode()

        message = aio_pika.Message(
            body=body,
            headers=headers,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Make messages persistent
        )
        try:
            await self._exchange.publish(message, routing_key=routing_key)
            logger.info(
                f"Published message to {self._exchange_name} with routing key '{routing_key}': {message}"
            )
        except Exception:
            logger.exception("Failed to publish message.")  # Log exception


class BusConsumer:
    def __init__(self, connection_url: str, exchange_name: str, queue_name: str):
        self._connection_url = connection_url
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._connection = None
        self._channel = None
        self._exchange = None
        self._queue = None
        self._callbacks = {}  # Store callbacks by event name
        self._running = False  # track if running

    async def connect(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self._connection_url)
            self._channel = await self._connection.channel()
            await self._channel.set_qos(
                prefetch_count=1
            )  # Process one message at a time
            self._exchange = await self._channel.declare_exchange(
                self._exchange_name, type=aio_pika.ExchangeType.HEADERS, durable=True
            )  # Ensure exchange is durable
            self._queue = await self._channel.declare_queue(
                self._queue_name, durable=False, auto_delete=True
            )  # Same settings
            await self._queue.bind(self._exchange)
            self._running = True  # Set to true.

    async def disconnect(self):
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
        self._running = False

    def subscribe(self, event_name: str, callback: Callable[[Any], Coroutine]):
        """Registers an async callback for a specific event.

        Args:
            event_name: The name of the event to subscribe to.
            callback: An async function (coroutine) to be called when the event is received.

        """
        # logger.info(f"Subscribing to the {event_name} event")
        if not asyncio.iscoroutinefunction(callback):
            raise ValueError("Callback must be a coroutine function (async def).")

        self._callbacks[event_name] = callback
        return callback

    async def on_message(self, message: AbstractIncomingMessage):
        """Handles incoming messages."""
        async with message.process(
            requeue=False
        ):  # Automatically acknowledge or reject (if exception) the message
            try:
                body = json.loads(message.body.decode())
                headers = message.headers
                await self._dispatcher(body, headers)  # dispatch
            except Exception:
                logger.exception(f"Error processing message: {message.body.decode()}")

    async def _dispatcher(self, body: dict, headers: dict):
        """Handles routing of events based on the name, and calls registered callbacks.
        """
        event_name = headers.get("name")
        if event_name and event_name in self._callbacks:
            try:
                await self._callbacks[event_name](body)
            except Exception:
                logger.exception(f"Error while processing event '{event_name}'")
        else:
            logger.warning(f"No handler found for event: {event_name}")

    async def run(self):
        """Starts consuming messages."""
        if not self._queue:
            await self.connect()  # Connect
        await self._queue.consume(self.on_message)
        print(f" [*] Waiting for messages on {self._queue_name}. To exit press CTRL+C")
        try:
            # Keep the consumer running.  aio-pika uses a separate thread.
            while self._running:
                await asyncio.sleep(1)  # use asyncio sleep.
        except Exception:
            logger.exception("Error while running")

    def stop(self):
        self._running = False


# --- FastAPI Dependency and Initialization ---

settings = get_settings()


async def get_bus_publisher() -> BusPublisher:
    # Return a publisher, it maintains the connection
    return BusPublisher(settings.bus.get_connection_url(), settings.bus.exchange_name)


async def get_bus_consumer() -> BusConsumer:
    # You might want a single, shared consumer instance for the entire app.
    # Create it lazily on first request.
    if not hasattr(get_bus_consumer, "consumer"):
        get_bus_consumer.consumer = BusConsumer(settings.bus.get_connection_url(), settings.bus.exchange_name, f"accent-chatd-{settings.uuid}")
    return get_bus_consumer.consumer


# Create a BusClient, to combine the publisher and consumer.
class BusClient:
    def __init__(self, publisher: BusPublisher, consumer: BusConsumer):
        self.publisher = publisher
        self.consumer = consumer


async def get_bus() -> BusClient:
    return BusClient(await get_bus_publisher(), await get_bus_consumer())
