# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import Any

from .base import Base
from .mixins import (
    AccentEventMixin,
    PublisherMixin,
    QueuePublisherMixin,
    ThreadableMixin,
)

logger = logging.getLogger(__name__)


class BusPublisher(AccentEventMixin, PublisherMixin, Base):
    def __init__(
        self,
        name: str | None = None,
        service_uuid: str | None = None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        **kwargs: Any,
    ):
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
    ThreadableMixin,
    QueuePublisherMixin,
    Base,
):
    def __init__(
        self,
        name: str | None = None,
        service_uuid: str | None = None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        **kwargs: Any,
    ):
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
