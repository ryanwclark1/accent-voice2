# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class HEPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'hep_general_edited'
    routing_key_fmt = 'config.hep_general.edited'

    def __init__(self) -> None:
        super().__init__()
