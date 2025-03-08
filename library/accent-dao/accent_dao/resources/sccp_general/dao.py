# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import daosession

from .persistor import SCCPGeneralPersistor


@daosession
def find_all(session):
    return SCCPGeneralPersistor(session).find_all()


@daosession
def edit_all(session, sccp_general):
    SCCPGeneralPersistor(session).edit_all(sccp_general)
