# Copyright 2023 Accent Communications

from accent_bus.resources.voicemail_general.event import VoicemailGeneralEditedEvent

from accent_confd import bus, sysconfd


class VoicemailGeneralNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def edited(self, voicemail_general):
        event = VoicemailGeneralEditedEvent()
        self.bus.queue_event(event)
        self.send_sysconfd_handlers(['voicemail reload'])


def build_notifier():
    return VoicemailGeneralNotifier(bus, sysconfd)
