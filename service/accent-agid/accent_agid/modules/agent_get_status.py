# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from accent_agid import agid
from accent_agid.handlers import agent

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor

    from accent_agid.agid import FastAGI

logger = logging.getLogger(__name__)


def agent_get_status(agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
    try:
        tenant_uuid = args[0]
        agent_id = int(args[1])

        agent.get_agent_status(agi, agent_id, tenant_uuid=tenant_uuid)
    except Exception as e:
        logger.exception("Error while getting agent status")
        agi.dp_break(e)


agid.register(agent_get_status)
