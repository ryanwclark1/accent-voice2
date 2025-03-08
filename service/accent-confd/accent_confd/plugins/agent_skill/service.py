# Copyright 2023 Accent Communications

from accent_dao.resources.agent import dao as agent_dao_module
from accent_dao.resources.skill import dao as skill_dao_module

from .notifier import build_notifier
from .validator import build_validator


class AgentMemberService:
    def __init__(self, agent_dao, skill_dao, validator, notifier):
        self.agent_dao = agent_dao
        self.skill_dao = skill_dao
        self.validator = validator
        self.notifier = notifier

    def find_agent_skill(self, agent, skill):
        for agent_skill in agent.agent_queue_skills:
            if agent_skill.skill == skill:
                return agent_skill
        return None

    def associate_agent_skill(self, agent, agent_skill):
        if agent_skill in agent.agent_queue_skills:
            return

        self.validator.validate_association(agent, agent_skill)
        self.agent_dao.associate_agent_skill(agent, agent_skill)
        self.notifier.skill_associated(agent, agent_skill)

    def dissociate_agent_skill(self, agent, agent_skill):
        if agent_skill not in agent.agent_queue_skills:
            return

        self.agent_dao.dissociate_agent_skill(agent, agent_skill)
        self.notifier.skill_dissociated(agent, agent_skill)


def build_service():
    return AgentMemberService(
        agent_dao_module, skill_dao_module, build_validator(), build_notifier()
    )
