# publisher.py
import logging
from typing import Any

import aiopika

from .base import Base
from .mixins import AiopikaConnectionMixin
from .schemas import Event
from .collectd.common import CollectdEvent  # Import CollectdEvent

logger = logging.getLogger(__name__)


class BusPublisher(AiopikaConnectionMixin, Base):
    """Asynchronous message publisher using aiopika."""

    def __init__(
        self,
        name: str | None = None,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672,
        exchange_name: str = "",
        exchange_type: str = "",
        service_uuid: str | None = None,
        **kwargs: Any,
    ):
        """
        Initializes the BusPublisher with connection parameters and optional service UUID.

        Args:
            name (str | None): Publisher name.
            username (str): RabbitMQ username.
            password (str): RabbitMQ password.
            host (str): RabbitMQ host.
            port (int): RabbitMQ port.
            exchange_name (str):  Exchange name.
            exchange_type (str):  Exchange type.
            service_uuid (str, optional): Unique identifier for this service instance.
            **kwargs:  Other parameters.
        """
        super().__init__(
            name, username, password, host, port, exchange_name, exchange_type, **kwargs
        )
        self.service_uuid = service_uuid  # Needed for collectd

    async def publish(
        self, event_name: str, event: Event, routing_key: str | None = None
    ) -> None:
        """Publishes an event to the configured RabbitMQ exchange.

        Args:
            event_name (str): The name of the event (for routing).
            event (Event): The event data (Pydantic model).
            routing_key (str, optional): The routing key. Defaults to event_name.
        """
        channel = await self.get_channel()
        exchange = await channel.declare_exchange(
            self._default_exchange_name, self._default_exchange_type
        )

        message_body = event.model_dump_json().encode()
        message = aiopika.Message(
            body=message_body,
            content_type="application/json",
            headers={"event_name": event_name},
        )

        await exchange.publish(message, routing_key=routing_key or event_name)
        logger.info(f"Published event: {event_name}, Data: {event.data}")

    async def publish_collectd(self, event: CollectdEvent) -> None:
        """Publishes a Collectd event.

        Args:
            event (CollectdEvent): The Collectd event to publish.
        """

        if not self.service_uuid:
            raise ValueError("service_uuid must be set for Collectd events")

        channel = await self.get_channel()
        exchange = await channel.declare_exchange(
            self._default_exchange_name, self._default_exchange_type
        )  # Or a dedicated collectd exchange

        payload: str = event.generate_payload(self.service_uuid)
        message = aiopika.Message(
            body=payload.encode(),
            content_type="text/plain",  # As per collectd network protocol
        )

        await exchange.publish(
            message, routing_key=event.routing_key_fmt
        )  # Use routing key from event
        logger.info(f"Published Collectd event: {event.name} - {payload}")
