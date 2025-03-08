# Copyright 2023 Accent Communications

from accent_dao.alchemy.application import Application
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult


class ApplicationPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = Application

    def __init__(self, session, application_search, tenant_uuids=None):
        self.session = session
        self.application_search = application_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(Application)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def search(self, parameters):
        query = self.session.query(self.application_search.config.table)
        query = self._filter_tenant_uuid(query)
        rows, total = self.application_search.search_from_query(query, parameters)
        return SearchResult(total, rows)
