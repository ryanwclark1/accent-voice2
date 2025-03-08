# Copyright 2023 Accent Communications

from accent_bus.resources.parking_lot.event import (
    ParkingLotCreatedEvent,
    ParkingLotDeletedEvent,
    ParkingLotEditedEvent,
)

from accent_confd import bus, sysconfd


class ParkingLotNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['module reload res_parking.so']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, parking_lot):
        self.send_sysconfd_handlers()
        event = ParkingLotCreatedEvent(parking_lot.id, parking_lot.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, parking_lot):
        self.send_sysconfd_handlers()
        event = ParkingLotEditedEvent(parking_lot.id, parking_lot.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, parking_lot):
        self.send_sysconfd_handlers()
        event = ParkingLotDeletedEvent(parking_lot.id, parking_lot.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return ParkingLotNotifier(bus, sysconfd)
