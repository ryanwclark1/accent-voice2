# Copyright 2023 Accent Communications

from accent_bus.resources.iax_callnumberlimits.event import IAXCallNumberLimitsEditedEvent

from accent_confd import bus, sysconfd


class IAXCallNumberLimitsNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def edited(self, iax_callnumberlimits):
        event = IAXCallNumberLimitsEditedEvent()
        self.bus.queue_event(event)
        self.send_sysconfd_handlers(['iax2 reload'])


def build_notifier():
    return IAXCallNumberLimitsNotifier(bus, sysconfd)
