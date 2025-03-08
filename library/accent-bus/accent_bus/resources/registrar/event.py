# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent
from .types import RegistrarDict


class RegistrarCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_created'
    routing_key_fmt = 'config.registrar.created'

    def __init__(self, registrar: RegistrarDict):
        super().__init__(registrar)


class RegistrarDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_deleted'
    routing_key_fmt = 'config.registrar.deleted'

    def __init__(self, registrar: RegistrarDict):
        super().__init__(registrar)


class RegistrarEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_edited'
    routing_key_fmt = 'config.registrar.edited'

    def __init__(self, registrar: RegistrarDict):
        super().__init__(registrar)
