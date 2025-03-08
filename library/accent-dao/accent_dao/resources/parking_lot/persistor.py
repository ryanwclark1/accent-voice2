# Copyright 2023 Accent Communications

from accent_dao.alchemy.parking_lot import ParkingLot
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin


class ParkingLotPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = ParkingLot

    def __init__(self, session, parking_lot_search, tenant_uuids=None):
        self.session = session
        self.search_system = parking_lot_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(ParkingLot)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def _search_query(self):
        return self.session.query(self.search_system.config.table)

    def delete(self, parking_lot):
        self._delete_associations(parking_lot)
        self.session.delete(parking_lot)
        self.session.flush()

    def _delete_associations(self, parking_lot):
        for extension in parking_lot.extensions:
            extension.type = 'user'
            extension.typeval = '0'
