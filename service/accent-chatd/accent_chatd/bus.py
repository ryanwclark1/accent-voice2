# Copyright 2023 Accent Communications

from accent.status import Status
from accent_bus.consumer import BusConsumer as BaseConsumer
from accent_bus.publisher import BusPublisher as BasePublisher


class BusConsumer(BaseConsumer):
    @classmethod
    def from_config(cls, bus_config):
        return cls(name='accent-chatd', **bus_config)

    def provide_status(self, status):
        status['bus_consumer']['status'] = (
            Status.ok if self.consumer_connected() else Status.fail
        )


class BusPublisher(BasePublisher):
    @classmethod
    def from_config(cls, service_uuid, bus_config):
        return cls(name='accent-chatd', service_uuid=service_uuid, **bus_config)
