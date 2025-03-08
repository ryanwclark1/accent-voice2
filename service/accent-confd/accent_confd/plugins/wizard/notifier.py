# Copyright 2023 Accent Communications

from accent_bus.resources.wizard.event import WizardCreatedEvent

from accent_confd import bus


class WizardNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self):
        event = WizardCreatedEvent()
        self.bus.queue_event(event)


def build_notifier():
    return WizardNotifier(bus)
