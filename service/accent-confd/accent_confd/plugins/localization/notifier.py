# Copyright 2023 Accent Communications

from accent_bus.resources.localization.event import LocalizationEditedEvent

from accent_confd import bus
from accent_confd.plugins.localization.schema import LocalizationSchema


class LocalizationNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, tenant):
        serialized = LocalizationSchema().dump(tenant)
        event = LocalizationEditedEvent(serialized, tenant.uuid)
        self.bus.queue_event(event)


def build_notifier():
    return LocalizationNotifier(bus)
