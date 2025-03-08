# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import AgentSkillRelation
from accent_confd_client.util import extract_id


class AgentRelation:
    def __init__(self, builder, agent_id):
        self.agent_id = agent_id
        self.agent_skill = AgentSkillRelation(builder)

    @extract_id
    def add_skill(self, skill_id, **kwargs):
        return self.agent_skill.associate(self.agent_id, skill_id, **kwargs)

    @extract_id
    def remove_skill(self, skill_id):
        return self.agent_skill.dissociate(self.agent_id, skill_id)


class AgentsCommand(MultiTenantCommand):
    resource = 'agents'
    relation_cmd = AgentRelation
