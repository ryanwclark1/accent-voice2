# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_agentd_client import error
from accent_agentd_client.error import AgentdClientError

from accent_agid.fastagi import FastAGI

AGENTSTATUS_VAR = 'ACCENT_AGENTSTATUS'


def login_agent(
    agi: FastAGI, agent_id: int, extension: str, context: str, tenant_uuid: str
) -> None:
    agentd_client = agi.config['agentd']['client']
    try:
        agentd_client.agents.login_agent(
            agent_id, extension, context, tenant_uuid=tenant_uuid
        )
    except AgentdClientError as e:
        if e.error == error.ALREADY_LOGGED:
            agi.set_variable(AGENTSTATUS_VAR, 'already_logged')
        elif e.error == error.ALREADY_IN_USE:
            agi.set_variable(AGENTSTATUS_VAR, 'already_in_use')
        else:
            raise
    else:
        agi.set_variable(AGENTSTATUS_VAR, 'logged')


def logoff_agent(agi: FastAGI, agent_id: int, tenant_uuid: str) -> None:
    agentd_client = agi.config['agentd']['client']
    try:
        agentd_client.agents.logoff_agent(agent_id, tenant_uuid=tenant_uuid)
    except AgentdClientError as e:
        if e.error != error.NOT_LOGGED:
            raise


def get_agent_status(agi: FastAGI, agent_id: int, tenant_uuid: str) -> None:
    agentd_client = agi.config['agentd']['client']
    status = agentd_client.agents.get_agent_status(agent_id, tenant_uuid=tenant_uuid)
    login_status = 'logged_in' if status.logged else 'logged_out'
    agi.set_variable('ACCENT_AGENT_LOGIN_STATUS', login_status)
