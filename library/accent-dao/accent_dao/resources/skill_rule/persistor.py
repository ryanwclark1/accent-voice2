# Copyright 2023 Accent Communications

from accent_dao.alchemy.queueskillrule import QueueSkillRule
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin


class SkillRulePersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = QueueSkillRule

    def __init__(self, session, skill_rule_search, tenant_uuids=None):
        self.session = session
        self.search_system = skill_rule_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(QueueSkillRule)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def get_by(self, criteria):
        model = self.find_by(criteria)
        if not model:
            raise errors.not_found('SkillRule', **criteria)
        return model

    def _search_query(self):
        return self.session.query(self.search_system.config.table)
