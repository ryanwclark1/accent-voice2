# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class IAXCallNumberLimitsEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'iax_callnumberlimits_edited'
    routing_key_fmt = 'config.iax_callnumberlimits.edited'

    def __init__(self) -> None:
        super().__init__()
