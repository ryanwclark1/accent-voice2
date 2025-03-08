# Copyright 2023 Accent Communications


from accent_dao.alchemy.user_external_app import UserExternalApp
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult


class UserExternalAppPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = UserExternalApp

    def __init__(self, session, user_external_app_search):
        self.session = session
        self.user_external_app_search = user_external_app_search

    def find_by(self, user_uuid, criteria):
        query = self._find_query(user_uuid, criteria)
        return query.first()

    def _find_query(self, user_uuid, criteria):
        query = self.session.query(UserExternalApp)
        query = query.filter(UserExternalApp.user_uuid == user_uuid)
        return self.build_criteria(query, criteria)

    def get_by(self, user_uuid, criteria):
        external_app = self.find_by(user_uuid, criteria)
        if not external_app:
            criteria['user_uuid'] = user_uuid
            raise errors.not_found('UserExternalApp', **criteria)
        return external_app

    def find_all_by(self, user_uuid, criteria):
        query = self._find_query(user_uuid, criteria)
        return query.all()

    def search(self, user_uuid, parameters):
        query = self.session.query(self.user_external_app_search.config.table)
        query = query.filter(UserExternalApp.user_uuid == user_uuid)
        rows, total = self.user_external_app_search.search_from_query(query, parameters)
        return SearchResult(total, rows)
