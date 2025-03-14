# accent_bus/publisher.py
# Copyright 2025 Accent Communications

"""AMQP Publisher."""

from __future__ import annotations

import logging
from typing import Any

from .base import Base
from .mixins import (
    AccentEventMixin,
    PublisherMixin,
    QueuePublisherMixin,
    # ThreadableMixin,  # Removed ThreadableMixin
)

logger = logging.getLogger(__name__)


class BusPublisher(AccentEventMixin, PublisherMixin, Base):
    """AMQP Bus Publisher."""

    def __init__(
        self,
        name: str | None = None,
        service_uuid: str | None = None,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672,
        exchange_name: str = "",
        exchange_type: str = "",
        **kwargs: Any,
    ) -> None:
        """Initialize the BusPublisher.

        Args:
           name: Publisher name.
           service_uuid: Service UUID.
           username: AMQP username.
           password: AMQP password.
           host: AMQP host.
           port: AMQP port.
           exchange_name: Exchange name.
           exchange_type: Exchange type.
           **kwargs: Additional keyword arguments.

        """
        super().__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            **kwargs,
        )


# Deprecated, thread should be avoided to respect WPEP-0004
class BusPublisherWithQueue(
    AccentEventMixin,
    # ThreadableMixin,  # Removed ThreadableMixin
    QueuePublisherMixin,
    Base,
):
    """AMQP Bus Publisher with Queue (Deprecated)."""

    def __init__(
        self,
        name: str | None = None,
        service_uuid: str | None = None,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672,
        exchange_name: str = "",
        exchange_type: str = "",
        **kwargs: Any,
    ) -> None:
        """Initialize BusPublisherWithQueue.

        Args:
           name: Publisher Name
           service_uuid: Service UUID
           username: AMQP Username
           password: AMQP Password
           host: AMQP Host
           port: AMQP Port
           exchange_name: Exchange Name
           exchange_type: Exchange Type
           **kwargs: Keyword Arguments

        """
        super().__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            **kwargs,
        )
