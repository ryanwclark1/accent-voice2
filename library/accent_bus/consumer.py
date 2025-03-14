# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Any

from .base import Base
from .mixins import (
    AccentEventMixin,
    ConsumerMixin,
    SubscribeExchangeDict,
    ThreadableMixin,
)


class BusConsumer(AccentEventMixin, ThreadableMixin, ConsumerMixin, Base):
    def __init__(
        self,
        name: str | None = None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        subscribe: SubscribeExchangeDict | None = None,
        **kwargs: Any,
    ):
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
