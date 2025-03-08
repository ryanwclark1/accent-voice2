# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class VoicemailZoneMessagesEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'voicemail_zonemessages_edited'
    routing_key_fmt = 'config.voicemail_zonemessages.edited'

    def __init__(self) -> None:
        super().__init__()
