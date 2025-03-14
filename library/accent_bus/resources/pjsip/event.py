# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent
from .types import PJSIPTransportDict


class PJSIPGlobalUpdatedEvent(ServiceEvent):
    service = 'confd'
    name = 'pjsip_global_updated'
    routing_key_fmt = 'config.pjsip_global.updated'

    def __init__(self) -> None:
        super().__init__()


class PJSIPSystemUpdatedEvent(ServiceEvent):
    service = 'confd'
    name = 'pjsip_system_updated'
    routing_key_fmt = 'config.pjsip_system.updated'

    def __init__(self) -> None:
        super().__init__()


class SIPTransportCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_transport_created'
    routing_key_fmt = 'config.sip.transports.created'

    def __init__(self, transport: PJSIPTransportDict):
        super().__init__(transport)


class SIPTransportDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_transport_deleted'
    routing_key_fmt = 'config.sip.transports.deleted'

    def __init__(self, transport: PJSIPTransportDict):
        super().__init__(transport)


class SIPTransportEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_transport_edited'
    routing_key_fmt = 'config.sip.transports.edited'

    def __init__(self, transport: PJSIPTransportDict):
        super().__init__(transport)
