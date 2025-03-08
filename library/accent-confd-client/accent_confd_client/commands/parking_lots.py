# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import ParkingLotExtensionRelation
from accent_confd_client.util import extract_id


class ParkingLotRelation:
    def __init__(self, builder, parking_lot_id):
        self.parking_lot_id = parking_lot_id
        self.parking_lot_extension = ParkingLotExtensionRelation(builder)

    @extract_id
    def add_extension(self, extension_id):
        return self.parking_lot_extension.associate(self.parking_lot_id, extension_id)

    @extract_id
    def remove_extension(self, extension_id):
        return self.parking_lot_extension.dissociate(self.parking_lot_id, extension_id)


class ParkingLotsCommand(MultiTenantCommand):
    resource = 'parkinglots'
    relation_cmd = ParkingLotRelation
