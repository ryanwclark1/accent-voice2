# Copyright 2023 Accent Communications

from accent.status import Status
from accent_bus.consumer import BusConsumer
from accent_bus.publisher import BusPublisher


class CoreBusConsumer(BusConsumer):
    @classmethod
    def from_config(cls, bus_config):
        name = 'accent-calld'
        return cls(name=name, **bus_config)

    def provide_status(self, status):
        status['bus_consumer']['status'] = (
            Status.ok if self.consumer_connected() else Status.fail
        )


class CoreBusPublisher(BusPublisher):
    @classmethod
    def from_config(cls, service_uuid, bus_config):
        name = 'accent-calld'
        return cls(name=name, service_uuid=service_uuid, **bus_config)
