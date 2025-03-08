# Copyright 2023 Accent Communications

from accent_bus.resources.device.event import (
    DeviceCreatedEvent,
    DeviceDeletedEvent,
    DeviceEditedEvent,
)

from accent_confd import bus


class DeviceNotifier:
    def __init__(self, bus, immediate=False):
        self.bus = bus
        self.immediate = immediate

    def created(self, device):
        event = DeviceCreatedEvent(device.id, device.tenant_uuid)
        self.send_bus_event(event)

    def edited(self, device):
        event = DeviceEditedEvent(device.id, device.tenant_uuid)
        self.send_bus_event(event)

    def deleted(self, device):
        event = DeviceDeletedEvent(device.id, device.tenant_uuid)
        self.send_bus_event(event)

    @property
    def send_bus_event(self):
        return self.bus.publish if self.immediate else self.bus.queue_event


def build_notifier():
    return DeviceNotifier(bus)
