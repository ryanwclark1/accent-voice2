# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class QueueGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'queue_general_edited'
    routing_key_fmt = 'config.queue_general.edited'

    def __init__(self) -> None:
        super().__init__()
