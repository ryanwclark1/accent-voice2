# core/consumer.py
import asyncio
import logging
from collections.abc import Callable, Coroutine
from typing import Any

from aiopika.abc import AbstractIncomingMessage
from pydantic import ValidationError

from .base import Base
from .mixins import AiopikaConnectionMixin

# NEW IMPORTS
from .schemas import Event

logger = logging.getLogger(__name__)


async def process_message(message: AbstractIncomingMessage) -> None:
    """Process an incoming message, attempting to parse it using Pydantic."""
    async with message.process():  # Acknowledge message upon *successful* processing
        try:
            event = Event.model_validate_json(message.body)
            logger.info("Received event: %s, Data: %s", event.name, event.data)
            # ... further processing (e.g., dispatch to handlers) ...
        except ValidationError as e:
            logger.error(f"Invalid message format: {e}")
            # Consider sending to a dead-letter queue (DLQ) here.
        except Exception:
            logger.exception("Error while processing message")


class BusConsumer(AiopikaConnectionMixin, Base):
    """Asynchronous message consumer using aiopika."""

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
    ):
        super().__init__(
            name, username, password, host, port, exchange_name, exchange_type, **kwargs
        )
        self.running = False  # Add a flag to control if consumer is running

    async def start_consuming(
        self,
        queue_name: str,
        event_name: str,
        callback: Callable[
            [AbstractIncomingMessage], Coroutine[Any, Any, None]
        ] = process_message,
    ) -> None:
        """Start the consumer to continuously listen for messages.

        Args:
            queue_name (str): The name of the queue.
            event_name (str): Event to bind to.
            callback (Callable): Callback function to process the message.

        """
        channel = await self.get_channel()
        await channel.set_qos(prefetch_count=1)  # Process one message at a time
        exchange = await channel.declare_exchange(
            self._default_exchange_name, self._default_exchange_type
        )  # Declare exchange
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        await queue.bind(exchange, routing_key=event_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await callback(message)

    async def run(self):
        """Start up the connection."""
        # Connection will close when this context manager exits.
        async with await self.get_connection():
            self.running = True
            while self.running:  # Keep the connection alive (simplified).
                await asyncio.sleep(1)  # Prevent busy-looping.

    async def stop(self):
        """Stop the running connection."""
        self.running = False
        if self._connection:
            await self._connection.close()
            self._connection = None
