# Copyright 2023 Accent Communications

from accent_dao.alchemy.staticiax import StaticIAX as RegisterIAX
from accent_dao.alchemy.trunkfeatures import TrunkFeatures
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult


class RegisterIAXPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = RegisterIAX

    def __init__(self, session, register_iax_search):
        self.session = session
        self.register_iax_search = register_iax_search

    def _find_query(self, criteria):
        query = self.session.query(RegisterIAX).filter(
            RegisterIAX.var_name == 'register'
        )
        return self.build_criteria(query, criteria)

    def get_by(self, criteria):
        model = self.find_by(criteria)
        if not model:
            raise errors.not_found('IAXRegister', **criteria)
        return model

    def search(self, parameters):
        rows, total = self.register_iax_search.search(self.session, parameters)
        return SearchResult(total, rows)

    def delete(self, register_iax):
        (
            self.session.query(TrunkFeatures)
            .filter(TrunkFeatures.register_iax_id == register_iax.id)
            .update({'registercommented': 0})
        )

        self.session.delete(register_iax)
        self.session.flush()
