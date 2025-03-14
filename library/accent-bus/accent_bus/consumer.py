# accent_bus/consumer.py
# Copyright 2025 Accent Communications

"""AMQP Consumer."""

from __future__ import annotations

from typing import Any, TypedDict

from .base import Base
from .mixins import (
    AccentEventMixin,
    ConsumerMixin,
    # ThreadableMixin,  # Removed ThreadableMixin
)


class SubscribeExchangeDict(TypedDict):
    """Exchange information."""

    exchange_name: str
    exchange_type: str


class BusConsumer(AccentEventMixin, ConsumerMixin, Base):
    """AMQP Bus Consumer."""

    def __init__(
        self,
        name: str | None = None,
        username: str = "guest",
        password: str = "guest",
        host: str = "localhost",
        port: int = 5672,
        exchange_name: str = "",
        exchange_type: str = "",
        subscribe: SubscribeExchangeDict | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the BusConsumer.

        Args:
           name (str, optional): Consumer name
           username (str, optional): AMQP Username
           password (str, optional): AMQP Password
           host (str, optional): AMQP Host
           port (int, optional): AMQP Port
           exchange_name (str, optional): exchange name to subscribe.
           exchange_type (str, optional): exchange type.
           subscribe (SubscribeExchangeDict, optional): Subscription details.
           **kwargs: Additional keyword arguments

        """
        super().__init__(
            name=name,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            subscribe=subscribe,
            **kwargs,
        )
