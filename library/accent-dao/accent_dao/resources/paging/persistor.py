# Copyright 2023 Accent Communications

from accent_dao.alchemy.paging import Paging
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin


class PagingPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = Paging

    def __init__(self, session, paging_search, tenant_uuids=None):
        self.session = session
        self.search_system = paging_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(Paging)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def _search_query(self):
        return self.session.query(self.search_system.config.table)
