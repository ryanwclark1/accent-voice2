# Copyright 2023 Accent Communications

from accent_dao.alchemy.conference import Conference
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin


class ConferencePersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = Conference

    def __init__(self, session, conference_search, tenant_uuids=None):
        self.session = session
        self.search_system = conference_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(Conference)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def _search_query(self):
        return self.session.query(self.search_system.config.table)

    def delete(self, conference):
        self._delete_associations(conference)
        self.session.delete(conference)
        self.session.flush()

    def _delete_associations(self, conference):
        for extension in conference.extensions:
            extension.type = 'user'
            extension.typeval = '0'
