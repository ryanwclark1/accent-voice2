# Copyright 2023 Accent Communications

from accent_bus.resources.queue_general.event import QueueGeneralEditedEvent

from accent_confd import bus, sysconfd


class QueueGeneralNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def edited(self, queue_general):
        event = QueueGeneralEditedEvent()
        self.bus.queue_event(event)
        self.send_sysconfd_handlers(['module reload app_queue.so'])


def build_notifier():
    return QueueGeneralNotifier(bus, sysconfd)
