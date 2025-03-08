# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import daosession

from .persistor import IAXCallNumberLimitsPersistor


@daosession
def find_all(session):
    return IAXCallNumberLimitsPersistor(session).find_all()


@daosession
def edit_all(session, iax_callnumberlimits):
    IAXCallNumberLimitsPersistor(session).edit_all(iax_callnumberlimits)
