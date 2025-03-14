# resources/common/mixins.py
import logging

import aiopika
from aiopika import RobustChannel, RobustConnection

logger = logging.getLogger(__name__)


class AiopikaConnectionMixin:
    """Mixin to provide aiopika connection and channel management."""

    _connection: RobustConnection | None = None
    _channel: RobustChannel | None = None

    async def get_connection(self) -> RobustConnection:
        """Get or creates an aiopika connection."""
        if self._connection is None or self._connection.is_closed:
            self._connection = await aiopika.connect_robust(self.url)
            logger.info(f"Connected to RabbitMQ: {self.url}")
        return self._connection

    async def get_channel(self) -> RobustChannel:
        """Get or creates an aiopika channel."""
        # Check the connection first
        if self._connection is None or self._connection.is_closed:
            self._connection = await aiopika.connect_robust(self.url)

        if self._channel is None or self._channel.is_closed:
            if self._connection:
                self._channel = await self._connection.channel()
            logger.info("RabbitMQ channel created.")
        return self._channel if self._channel else await self.get_connection().channel()
