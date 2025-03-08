# Copyright 2023 Accent Communications

from accent_dao.resources.extension import dao as extension_dao
from accent_dao.resources.parking_lot import dao as parking_lot_dao

from .resource import ParkingLotExtensionItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            ParkingLotExtensionItem,
            '/parkinglots/<int:parking_lot_id>/extensions/<int:extension_id>',
            endpoint='parking_lot_extensions',
            resource_class_args=(service, parking_lot_dao, extension_dao),
        )
