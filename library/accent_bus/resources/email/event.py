# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class EmailConfigUpdatedEvent(ServiceEvent):
    service = 'confd'
    name = 'email_config_updated'
    routing_key_fmt = 'config.email.updated'

    def __init__(self) -> None:
        super().__init__()
