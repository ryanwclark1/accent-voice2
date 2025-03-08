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


def agent_logoff(agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
    try:
        tenant_uuid = args[0]
        agent_id = int(args[1])

        agent.logoff_agent(agi, agent_id, tenant_uuid=tenant_uuid)
    except Exception as e:
        logger.exception("Error while logging off agent")
        agi.dp_break(e)


agid.register(agent_logoff)
