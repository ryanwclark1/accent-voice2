# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import daosession

from .persistor import VoicemailGeneralPersistor


@daosession
def find_all(session):
    return VoicemailGeneralPersistor(session).find_all()


@daosession
def edit_all(session, voicemail_general):
    VoicemailGeneralPersistor(session).edit_all(voicemail_general)
