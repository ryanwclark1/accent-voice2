# Copyright 2023 Accent Communications

from accent_bus.resources.sccp_general.event import SCCPGeneralEditedEvent

from accent_confd import bus, sysconfd


class SCCPGeneralNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def edited(self, sccp_general):
        event = SCCPGeneralEditedEvent()
        self.bus.queue_event(event)
        self.send_sysconfd_handlers(['module reload chan_sccp.so'])


def build_notifier():
    return SCCPGeneralNotifier(bus, sysconfd)
