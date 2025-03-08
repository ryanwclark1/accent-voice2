# Copyright 2023 Accent Communications

from accent_dao.alchemy.infos import Infos
from accent_dao.helpers.db_manager import daosession
from accent_dao.helpers.db_utils import flush_session


@daosession
def is_live_reload_enabled(session):
    infos = session.query(Infos).first()
    return infos.live_reload_enabled


@daosession
def set_live_reload_status(session, data):
    value = data['enabled']
    with flush_session(session):
        session.query(Infos).update({'live_reload_enabled': value})
