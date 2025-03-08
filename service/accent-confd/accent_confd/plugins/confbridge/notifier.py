# Copyright 2023 Accent Communications

from accent_bus.resources.confbridge.event import (
    ConfBridgeAccentDefaultBridgeEditedEvent,
    ConfBridgeAccentDefaultUserEditedEvent,
)

from accent_confd import bus, sysconfd


class ConfBridgeConfigurationNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def edited(self, section_name, confbridge):
        if section_name == 'accent_default_bridge':
            event = ConfBridgeAccentDefaultBridgeEditedEvent()
            self.bus.queue_event(event)
        elif section_name == 'accent_default_user':
            event = ConfBridgeAccentDefaultUserEditedEvent()
            self.bus.queue_event(event)

        self.send_sysconfd_handlers(['module reload app_confbridge.so'])


def build_notifier():
    return ConfBridgeConfigurationNotifier(bus, sysconfd)
