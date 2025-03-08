# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import daosession

from .persistor import IAXGeneralPersistor


@daosession
def find_all(session):
    return IAXGeneralPersistor(session).find_all()


@daosession
def edit_all(session, iax_general):
    IAXGeneralPersistor(session).edit_all(iax_general)
