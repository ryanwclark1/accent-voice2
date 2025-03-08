# Copyright 2023 Accent Communications

from accent_dao.alchemy.schedule import Schedule
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin


class SchedulePersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = Schedule

    def __init__(self, session, schedule_search, tenant_uuids=None):
        self.session = session
        self.search_system = schedule_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(Schedule)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def _search_query(self):
        return self.session.query(self.search_system.config.table)
