# Copyright 2023 Accent Communications

from accent_bus.resources.register.event import (
    RegisterIAXCreatedEvent,
    RegisterIAXDeletedEvent,
    RegisterIAXEditedEvent,
)

from accent_confd import bus, sysconfd


class RegisterIAXNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['iax2 reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, register):
        self.send_sysconfd_handlers()
        event = RegisterIAXCreatedEvent(register.id)
        self.bus.queue_event(event)

    def edited(self, register):
        self.send_sysconfd_handlers()
        event = RegisterIAXEditedEvent(register.id)
        self.bus.queue_event(event)

    def deleted(self, register):
        self.send_sysconfd_handlers()
        event = RegisterIAXDeletedEvent(register.id)
        self.bus.queue_event(event)


def build_notifier():
    return RegisterIAXNotifier(bus, sysconfd)
