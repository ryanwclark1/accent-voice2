# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class WizardCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'wizard_created'
    routing_key_fmt = 'config.wizard.created'

    def __init__(self) -> None:
        super().__init__()
