# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from accent_agid import agid, objects

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor

    from accent_agid.agid import FastAGI

logger = logging.getLogger(__name__)


def agent_get_options(agi: FastAGI, cursor: DictCursor, args: list[str]) -> None:
    agi.set_variable('ACCENT_AGENTEXISTS', 0)

    try:
        tenant_uuid = args[0]
        number = str(args[1])

        if number.startswith('*'):
            agent_id = number[1:]
            agent = objects.Agent.from_id(cursor, agent_id, tenant_uuid)
        else:
            agent = objects.Agent.from_number(cursor, number, tenant_uuid)
    except (LookupError, IndexError) as e:
        agi.verbose(str(e))
        return

    agi.set_variable('ACCENT_AGENTEXISTS', 1)
    agi.set_variable('ACCENT_AGENTPASSWD', agent.passwd or '')
    agi.set_variable('ACCENT_AGENTID', agent.id)
    agi.set_variable('ACCENT_AGENTNUM', agent.number)

    if agent.language:
        agi.set_variable('CHANNEL(language)', agent.language)


agid.register(agent_get_options)
