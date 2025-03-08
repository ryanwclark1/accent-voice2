# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class VoicemailGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'voicemail_general_edited'
    routing_key_fmt = 'config.voicemail_general.edited'

    def __init__(self) -> None:
        super().__init__()
