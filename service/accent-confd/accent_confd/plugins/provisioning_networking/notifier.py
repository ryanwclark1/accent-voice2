# Copyright 2023 Accent Communications

from accent_bus.resources.provisioning_networking.event import (
    ProvisioningNetworkingEditedEvent,
)


class ProvisioningNetworkingNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def edited(self, provisioning_networking):
        event = ProvisioningNetworkingEditedEvent()
        self.bus.queue_event(event)
        self.sysconfd.commonconf_generate()
        self.sysconfd.commonconf_apply()
        self.sysconfd.restart_provd()
