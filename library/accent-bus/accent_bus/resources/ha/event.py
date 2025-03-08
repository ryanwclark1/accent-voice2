# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class HAEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'ha_edited'
    routing_key_fmt = 'config.ha.edited'

    def __init__(self) -> None:
        super().__init__()
