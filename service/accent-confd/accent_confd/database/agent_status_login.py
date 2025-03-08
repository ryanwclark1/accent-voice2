# Copyright 2023 Accent Communications

from accent_dao.alchemy.agent_login_status import AgentLoginStatus
from accent_dao.helpers.db_manager import Session


def find_by(**kwargs):
    return Session.query(AgentLoginStatus).filter_by(**kwargs).first()
