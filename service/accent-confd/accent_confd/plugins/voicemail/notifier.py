# Copyright 2023 Accent Communications

from accent_bus.resources.voicemail.event import (
    UserVoicemailEditedEvent,
    VoicemailCreatedEvent,
    VoicemailDeletedEvent,
    VoicemailEditedEvent,
)

from accent_confd import bus, sysconfd


class VoicemailNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def _send_sysconfd_handlers(self, ipbx_commands):
        handlers = {'ipbx': ipbx_commands}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, voicemail):
        self._send_sysconfd_handlers(['voicemail reload'])
        event = VoicemailCreatedEvent(voicemail.id, voicemail.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, voicemail):
        self._send_sysconfd_handlers(
            [
                'voicemail reload',
                'module reload res_pjsip.so',
                'module reload chan_sccp.so',
            ]
        )
        event = VoicemailEditedEvent(voicemail.id, voicemail.tenant_uuid)
        self.bus.queue_event(event)

        for user in voicemail.users:
            event = UserVoicemailEditedEvent(
                voicemail.id, voicemail.tenant_uuid, user.uuid
            )
            self.bus.queue_event(event)

    def deleted(self, voicemail):
        self._send_sysconfd_handlers(['voicemail reload'])
        event = VoicemailDeletedEvent(voicemail.id, voicemail.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return VoicemailNotifier(bus, sysconfd)
