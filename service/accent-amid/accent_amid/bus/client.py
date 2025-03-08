# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent.status import Status, StatusDict
from accent_bus.publisher import BusPublisherWithQueue
from accent_bus.resources.ami.event import AMIEvent

if TYPE_CHECKING:
    from ..ami.client import Message
    from ..config import BusConfigDict


class BusClient(BusPublisherWithQueue):
    @classmethod
    def from_config(cls, service_uuid: str, bus_config: BusConfigDict) -> BusClient:
        name = 'accent-amid'
        return cls(name=name, service_uuid=service_uuid, **bus_config)

    def provide_status(self, status: StatusDict) -> None:
        status['bus_publisher']['status'] = (
            Status.ok if self.queue_publisher_connected() else Status.fail
        )

    def publish(self, *messages: Message) -> None:
        for message in messages:
            super().publish_soon(AMIEvent(message.name, message.headers))
