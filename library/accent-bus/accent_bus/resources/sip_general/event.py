# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class SIPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_general_edited'
    routing_key_fmt = 'config.sip_general.edited'

    def __init__(self) -> None:
        super().__init__()
