# Copyright 2023 Accent Communications

from accent_bus.base import Base
from accent_bus.mixins import CollectdMixin, QueuePublisherMixin, ThreadableMixin


class CollectdPublisher(CollectdMixin, QueuePublisherMixin, ThreadableMixin, Base):
    @classmethod
    def from_config(cls, service_uuid, bus_config, collectd_config):
        config = dict(bus_config)
        config.update(**collectd_config)
        return cls(name='collectd', service_uuid=service_uuid, **config)
