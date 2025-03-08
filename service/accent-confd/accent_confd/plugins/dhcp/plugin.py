# Copyright 2023 Accent Communications

from accent_confd import bus, sysconfd

from .notifier import DHCPNotifier
from .resource import DHCPResource
from .service import DHCPService


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        notifier = DHCPNotifier(bus, sysconfd)
        service = DHCPService(notifier, sysconfd)

        api.add_resource(DHCPResource, '/dhcp', resource_class_args=(service,))
