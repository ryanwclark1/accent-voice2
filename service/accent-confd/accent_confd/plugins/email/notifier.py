# Copyright 2023 Accent Communications

from accent_bus.resources.email.event import EmailConfigUpdatedEvent


class EmailConfigNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def edited(self):
        event = EmailConfigUpdatedEvent()
        self.bus.queue_event(event)
        self.sysconfd.commonconf_generate()
        self.sysconfd.commonconf_apply()
