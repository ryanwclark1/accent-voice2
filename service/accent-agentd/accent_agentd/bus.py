# Copyright 2023 Accent Communications

from accent.status import Status
from accent_bus.consumer import BusConsumer as Consumer
from accent_bus.publisher import BusPublisher as Publisher
from accent_bus.resources.ami.event import AMIEvent


class BusConsumer(Consumer):
    @classmethod
    def from_config(cls, bus_config):
        name = 'accent-agentd'
        return cls(name=name, **bus_config)

    def provide_status(self, status):
        status['bus_consumer']['status'] = (
            Status.ok if self.consumer_connected() else Status.fail
        )


class BusPublisher(Publisher):
    @classmethod
    def from_config(cls, service_uuid, bus_config):
        name = 'accent-agentd'
        return cls(name=name, service_uuid=service_uuid, **bus_config)


class QueueMemberPausedEvent(AMIEvent):
    name = 'QueueMemberPause'
