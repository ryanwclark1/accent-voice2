# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import daosession

from .persistor import ParkingLotPersistor
from .search import parking_lot_search


@daosession
def search(session, tenant_uuids=None, **parameters):
    return ParkingLotPersistor(session, parking_lot_search, tenant_uuids).search(
        parameters
    )


@daosession
def get(session, parking_lot_id, tenant_uuids=None):
    return ParkingLotPersistor(session, parking_lot_search, tenant_uuids).get_by(
        {'id': parking_lot_id}
    )


@daosession
def get_by(session, tenant_uuids=None, **criteria):
    return ParkingLotPersistor(session, parking_lot_search, tenant_uuids).get_by(
        criteria
    )


@daosession
def find(session, parking_lot_id, tenant_uuids=None):
    return ParkingLotPersistor(session, parking_lot_search, tenant_uuids).find_by(
        {'id': parking_lot_id}
    )


@daosession
def find_by(session, tenant_uuids=None, **criteria):
    return ParkingLotPersistor(session, parking_lot_search, tenant_uuids).find_by(
        criteria
    )


@daosession
def find_all_by(session, tenant_uuids=None, **criteria):
    return ParkingLotPersistor(session, parking_lot_search, tenant_uuids).find_all_by(
        criteria
    )


@daosession
def create(session, parking_lot):
    return ParkingLotPersistor(session, parking_lot_search).create(parking_lot)


@daosession
def edit(session, parking_lot):
    ParkingLotPersistor(session, parking_lot_search).edit(parking_lot)


@daosession
def delete(session, parking_lot):
    ParkingLotPersistor(session, parking_lot_search).delete(parking_lot)
