# Copyright 2023 Accent Communications


from accent_dao.alchemy.infos import Infos
from accent_dao.helpers import errors
from accent_dao.helpers.db_manager import daosession


@daosession
def get(session):
    row = (session.query(Infos).first())

    if not row:
        raise errors.not_found('Infos')
    return row
