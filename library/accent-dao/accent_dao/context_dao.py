# Copyright 2023 Accent Communications

from accent_dao.alchemy.context import Context
from accent_dao.helpers.db_manager import daosession


@daosession
def get(session, context_name):
    return session.query(Context).filter(Context.name == context_name).first()
