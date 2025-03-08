# Copyright 2023 Accent Communications

from accent_bus.resources.configuration.event import LiveReloadEditedEvent

from accent_confd import bus


class LiveReloadNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, live_reload):
        event = LiveReloadEditedEvent(live_reload['enabled'])
        self.bus.queue_event(event)


def build_notifier():
    return LiveReloadNotifier(bus)
