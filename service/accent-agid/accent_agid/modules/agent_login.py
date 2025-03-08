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


def agent_login(agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
    try:
        tenant_uuid = args[0]
        agent_id = int(args[1])
        extension = args[2]
        context = args[3]

        agent.login_agent(agi, agent_id, extension, context, tenant_uuid)
    except Exception as e:
        logger.exception("Error while logging in agent")
        agi.dp_break(e)


agid.register(agent_login)
