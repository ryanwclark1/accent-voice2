# Copyright 2023 Accent Communications

from accent_bus.publisher import BusPublisher as Publisher


class BusPublisher(Publisher):
    def __init__(self, service_uuid=None, **kwargs):
        name = 'accent-auth'
        self._url = kwargs.pop('uri', None)
        super().__init__(name, service_uuid, **kwargs)

    @classmethod
    def from_config(cls, service_uuid, bus_config):
        return cls(service_uuid=service_uuid, **bus_config)

    @property
    def url(self):
        return self._url
