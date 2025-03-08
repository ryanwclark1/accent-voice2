# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.helpers.validator import ValidationAssociation, ValidatorAssociation


class UserAgentAssociationValidator(ValidatorAssociation):
    def validate(self, user, agent):
        self.validate_same_tenant(user, agent)
        self.validate_user_not_already_associated(user, agent)

    def validate_same_tenant(self, user, agent):
        if agent.tenant_uuid != user.tenant_uuid:
            raise errors.different_tenants(
                agent_tenant_uuid=agent.tenant_uuid, user_tenant_uuid=user.tenant_uuid
            )

    def validate_user_not_already_associated(self, user, agent):
        if user.agentid:
            raise errors.resource_associated(
                'User', 'Agent', user_id=user.id, agent=agent.id
            )


def build_validator():
    return ValidationAssociation(association=[UserAgentAssociationValidator()])
