# Copyright 2023 Accent Communications

from accent_dao.resources.user import dao as user_dao

from accent_confd.plugins.user_agent.notifier import build_notifier
from accent_confd.plugins.user_agent.validator import build_validator


class UserAgentService:
    def __init__(self, dao, validator, notifier):
        self.dao = dao
        self.validator = validator
        self.notifier = notifier

    def associate(self, user, agent):
        if agent.id == user.agent_id:
            return

        self.validator.validate_association(user, agent)
        user.agent_id = agent.id
        self.dao.edit(user)
        self.notifier.associated(user, agent)

    def dissociate(self, user):
        agent = user.agent
        if not agent:
            return

        self.validator.validate_dissociation(user, agent)
        user.agent_id = None
        self.dao.edit(user)
        self.notifier.dissociated(user, agent)


def build_service():
    return UserAgentService(user_dao, build_validator(), build_notifier())
