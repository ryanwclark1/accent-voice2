# src/accent_amid/services/ami.py
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, NoReturn

from accent_amid.ami.client import AMIClient, AMIConnectionError, Message

if TYPE_CHECKING:
    from collections import deque

    from accent_auth_client import Client as AuthClient
    from accent_bus.publisher import BusPublisherWithQueue

    from accent_amid.config import Settings

logger = logging.getLogger(__name__)


class AMIService:
    """Service for managing the AMI client and its interaction with the message bus.

    This service encapsulates the AMI connection, message handling, and
    reconnection logic.  It publishes received AMI messages to the bus.

    Attributes:
        RECONNECTION_DELAY (int): delay for reconnection.
        _config (Settings): configuration.
        _ami_client (AMIClient): client.
        _bus_client (BusPublisherWithQueue): bus client.
        _stop_event (asyncio.Event): stop event.

    """

    RECONNECTION_DELAY = 5

    def __init__(
        self,
        config: Settings,
        bus_client: BusPublisherWithQueue,
        auth_client: AuthClient,
    ) -> None:
        """Initialize AMIService.

        Args:
            config (Settings): application settings.
            bus_client (BusPublisherWithQueue): client.
            auth_client (AuthClient): client.

        """
        self._config = config
        self._ami_client = AMIClient(
            host=config.ami.HOST,
            username=config.ami.USERNAME,
            password=config.ami.PASSWORD,
            port=config.ami.PORT,
        )
        self._bus_client = bus_client
        self._auth_client = auth_client
        self._stop_event = asyncio.Event()

    async def run(self) -> None:
        """Run main loop for the AMIService.

        Connects to the AMI, continuously processes messages, and handles
        reconnection.  Runs until `stop()` is called.
        """
        await self._bus_client.connect()
        while not self._stop_event.is_set():
            try:
                await self._ami_client.connect_and_login()
                await self._process_messages_indefinitely()
            except AMIConnectionError as e:
                await self._handle_ami_connection_error(e)
            except Exception as e:
                await self._handle_unexpected_error(e)

    async def _handle_ami_connection_error(self, e: AMIConnectionError) -> None:
        """Handle AMI connection errors, disconnecting and waiting before retrying."""
        await self._ami_client.disconnect(reason=e.error)
        try:
            await asyncio.wait_for(
                self._stop_event.wait(), timeout=self.RECONNECTION_DELAY
            )
        except TimeoutError:
            pass  # Expected - continue with reconnection attempt

    async def _handle_unexpected_error(self, e: Exception) -> NoReturn:
        """Handle unexpected errors, disconnecting and raising the exception."""
        await self._ami_client.disconnect(reason=f"Unexpected error: {e}")
        raise

    async def _process_messages_indefinitely(self) -> None:
        """Continuously parses and processes messages from the AMI."""
        while not self._stop_event.is_set():
            new_messages = await self._ami_client.parse_next_messages()
            await self._process_messages(new_messages)

    async def _process_messages(self, messages: deque[Message]) -> None:
        """Process a deque of AMI messages, publishing them to the bus."""
        while len(messages):
            message = messages.pop()
            logger.debug("Processing message %s", message)
            await self._bus_client.publish(message.name, message.headers)

    async def stop(self) -> None:
        """Stop the AMIService gracefully."""
        logger.info("Stopping AMIService...")
        self._stop_event.set()
        await self._ami_client.stop()
        await self._bus_client.close_connection()
        logger.info("AMIService stopped.")

    async def __aenter__(self) -> AMIService:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.stop()
