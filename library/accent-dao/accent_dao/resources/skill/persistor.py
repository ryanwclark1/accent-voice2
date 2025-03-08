# Copyright 2023 Accent Communications

from accent_dao.alchemy.queueskill import QueueSkill
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin


class SkillPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = QueueSkill

    def __init__(self, session, skill_search, tenant_uuids=None):
        self.session = session
        self.search_system = skill_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(QueueSkill)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    def get_by(self, criteria):
        model = self.find_by(criteria)
        if not model:
            raise errors.not_found('Skill', **criteria)
        return model

    def _search_query(self):
        return self.session.query(self.search_system.config.table)

    def create(self, skill):
        self.session.add(skill)
        self.session.flush()
        return skill

    def edit(self, skill):
        self.session.add(skill)
        self.session.flush()
