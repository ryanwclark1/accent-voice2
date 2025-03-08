# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class AgentSkillAssociationValidator(ValidatorAssociation):
    def validate(self, agent, agent_queue_skill):
        self.validate_same_tenant(agent, agent_queue_skill.skill)

    def validate_same_tenant(self, agent, skill):
        if agent.tenant_uuid != skill.tenant_uuid:
            raise errors.different_tenants(
                agent_tenant_uuid=agent.tenant_uuid, skill_tenant_uuid=skill.tenant_uuid
            )


def build_validator():
    return ValidationAssociation(association=[AgentSkillAssociationValidator()])
