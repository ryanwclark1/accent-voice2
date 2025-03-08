# Copyright 2023 Accent Communications

from accent_bus.resources.voicemail_zonemessages.event import (
    VoicemailZoneMessagesEditedEvent,
)

from accent_confd import bus, sysconfd


class VoicemailZoneMessagesNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def edited(self, voicemail_zonemessages):
        event = VoicemailZoneMessagesEditedEvent()
        self.bus.queue_event(event)
        self.send_sysconfd_handlers(['voicemail reload'])


def build_notifier():
    return VoicemailZoneMessagesNotifier(bus, sysconfd)
