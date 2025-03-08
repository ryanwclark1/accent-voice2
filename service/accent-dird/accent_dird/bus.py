# Copyright 2023 Accent Communications

from accent.status import Status
from accent_bus.consumer import BusConsumer
from accent_bus.publisher import BusPublisher


class CoreBus(BusPublisher, BusConsumer):
    def __init__(
        self,
        service_uuid,
        enabled=True,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        **kwargs,
    ):
        name = 'accent-dird'
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
        self.enabled = enabled

    def provide_status(self, status):
        status['bus_consumer']['status'] = Status.ok if self.consumer_connected() else Status.fail

    def publish(self, event, extra_headers=None, payload=None):
        if not self.enabled:
            return
        super().publish(event, extra_headers, payload)

    def start(self):
        if not self.enabled:
            return
        super().start()
