# Copyright 2023 Accent Communications

import logging

from accent import debug
from accent_dao.helpers import db_utils

logger = logging.getLogger(__name__)


class PauseHandler:
    def __init__(self, pause_manager, agent_status_dao):
        self._pause_manager = pause_manager
        self._agent_status_dao = agent_status_dao

    @debug.trace_duration
    def handle_pause_by_number(self, agent_number, reason, tenant_uuids=None):
        logger.info('Executing pause command (number %s)', agent_number)
        with db_utils.session_scope():
            agent_status = self._agent_status_dao.get_status_by_number(
                agent_number, tenant_uuids=tenant_uuids
            )
        self._pause_manager.pause_agent(agent_status, reason)

    @debug.trace_duration
    def handle_unpause_by_number(self, agent_number, tenant_uuids=None):
        logger.info('Executing unpause command (number %s)', agent_number)
        with db_utils.session_scope():
            agent_status = self._agent_status_dao.get_status_by_number(
                agent_number, tenant_uuids=tenant_uuids
            )
        self._pause_manager.unpause_agent(agent_status)

    @debug.trace_duration
    def handle_pause_user_agent(self, user_uuid, reason, tenant_uuids=None):
        logger.info('Executing pause command (agent of user %s)', user_uuid)
        with db_utils.session_scope():
            agent_status = self._agent_status_dao.get_status_by_user(
                user_uuid, tenant_uuids=tenant_uuids
            )
        self._pause_manager.pause_user_agent(
            user_uuid, agent_status, reason, tenant_uuids=tenant_uuids
        )

    @debug.trace_duration
    def handle_unpause_user_agent(self, user_uuid, tenant_uuids=None):
        logger.info('Executing unpause command (agent of user %s)', user_uuid)
        with db_utils.session_scope():
            agent_status = self._agent_status_dao.get_status_by_user(
                user_uuid, tenant_uuids=tenant_uuids
            )
        self._pause_manager.unpause_user_agent(
            user_uuid, agent_status, tenant_uuids=tenant_uuids
        )
