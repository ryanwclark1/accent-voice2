# Copyright 2023 Accent Communications

from accent_dao.resources.agent import dao as agent_dao

from accent_confd.helpers.resource import CRUDService

from .notifier import build_notifier
from .validator import build_validator


class AgentFeaturesService(CRUDService):
    def create(self, agent_features):
        self.validator.validate_create(
            agent_features, tenant_uuids=[agent_features.tenant_uuid]
        )
        created_agent_features = self.dao.create(agent_features)
        self.notifier.created(created_agent_features)
        return created_agent_features


def build_service():
    return AgentFeaturesService(agent_dao, build_validator(), build_notifier())
