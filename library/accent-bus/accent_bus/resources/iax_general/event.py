# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class IAXGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'iax_general_edited'
    routing_key_fmt = 'config.iax_general.edited'

    def __init__(self) -> None:
        super().__init__()
