# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class ParkingLotCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_created'
    routing_key_fmt = 'config.parkinglots.created'

    def __init__(self, parking_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(parking_id)}
        super().__init__(content, tenant_uuid)


class ParkingLotDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_deleted'
    routing_key_fmt = 'config.parkinglots.deleted'

    def __init__(self, parking_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(parking_id)}
        super().__init__(content, tenant_uuid)


class ParkingLotEditedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_edited'
    routing_key_fmt = 'config.parkinglots.edited'

    def __init__(self, parking_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(parking_id)}
        super().__init__(content, tenant_uuid)
