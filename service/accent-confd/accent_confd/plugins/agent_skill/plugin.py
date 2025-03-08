# Copyright 2023 Accent Communications

from accent_dao.resources.agent import dao as agent_dao
from accent_dao.resources.skill import dao as skill_dao

from .resource import AgentSkillItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            AgentSkillItem,
            '/agents/<int:agent_id>/skills/<int:skill_id>',
            endpoint='agent_skills',
            resource_class_args=(service, agent_dao, skill_dao),
        )
