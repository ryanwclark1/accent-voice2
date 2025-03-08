# Copyright 2023 Accent Communications

import logging

from accent import debug

logger = logging.getLogger(__name__)


class RelogHandler:
    def __init__(self, relog_manager):
        self._relog_manager = relog_manager

    @debug.trace_duration
    def handle_relog_all(self, tenant_uuids=None):
        logger.info('Executing relog all command')
        self._relog_manager.relog_all_agents(tenant_uuids=tenant_uuids)
