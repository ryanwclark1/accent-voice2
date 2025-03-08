# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class SCCPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'sccp_general_edited'
    routing_key_fmt = 'config.sccp_general.edited'

    def __init__(self) -> None:
        super().__init__()
