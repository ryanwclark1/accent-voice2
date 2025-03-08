# Copyright 2023 Accent Communications


from accent_dao.alchemy.staticvoicemail import StaticVoicemail
from accent_dao.helpers.db_manager import Session


def find_all_timezone():
    rows = (
        Session.query(StaticVoicemail.var_name)
        .filter(StaticVoicemail.category == 'zonemessages')
        .all()
    )

    return [row.var_name for row in rows]
