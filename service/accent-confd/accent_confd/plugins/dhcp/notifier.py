# Copyright 2023 Accent Communications

from accent_bus.resources.dhcp.event import DHCPEditedEvent

from accent_confd._bus import BusPublisher
from accent_confd._sysconfd import SysconfdPublisher


class DHCPNotifier:
    def __init__(self, bus, sysconfd):
        self.bus: BusPublisher = bus
        self.sysconfd: SysconfdPublisher = sysconfd

    def edited(self):
        event = DHCPEditedEvent()
        self.bus.queue_event(event)
        self.sysconfd.commonconf_generate()
        self.sysconfd.commonconf_apply()
