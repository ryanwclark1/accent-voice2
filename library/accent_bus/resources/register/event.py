# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class RegisterSIPCreated(ServiceEvent):
    service = 'confd'
    name = 'register_sip_created'
    routing_key_fmt = 'config.register.sip.created'

    def __init__(self, register_id: int):
        content = {'id': int(register_id)}
        super().__init__(content)


class RegisterSIPDeleted(ServiceEvent):
    service = 'confd'
    name = 'register_sip_deleted'
    routing_key_fmt = 'config.register.sip.deleted'

    def __init__(self, register_id: int):
        content = {'id': int(register_id)}
        super().__init__(content)


class RegisterSIPEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_sip_edited'
    routing_key_fmt = 'config.register.sip.edited'

    def __init__(self, register_id: int):
        content = {'id': int(register_id)}
        super().__init__(content)


class RegisterIAXCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_iax_created'
    routing_key_fmt = 'config.register.iax.created'

    def __init__(self, register_id: int):
        content = {'id': int(register_id)}
        super().__init__(content)


class RegisterIAXDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_iax_deleted'
    routing_key_fmt = 'config.register.iax.deleted'

    def __init__(self, register_id: int):
        content = {'id': int(register_id)}
        super().__init__(content)


class RegisterIAXEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_iax_edited'
    routing_key_fmt = 'config.register.iax.edited'

    def __init__(self, register_id: int):
        content = {'id': int(register_id)}
        super().__init__(content)
