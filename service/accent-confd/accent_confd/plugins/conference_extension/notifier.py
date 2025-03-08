# Copyright 2023 Accent Communications

from accent_bus.resources.conference_extension.event import (
    ConferenceExtensionAssociatedEvent,
    ConferenceExtensionDissociatedEvent,
)

from accent_confd import bus, sysconfd


class ConferenceExtensionNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['dialplan reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def associated(self, conference, extension):
        self.send_sysconfd_handlers()
        event = ConferenceExtensionAssociatedEvent(
            conference.id, extension.id, conference.tenant_uuid
        )
        self.bus.queue_event(event)

    def dissociated(self, conference, extension):
        self.send_sysconfd_handlers()
        event = ConferenceExtensionDissociatedEvent(
            conference.id, extension.id, conference.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return ConferenceExtensionNotifier(bus, sysconfd)
