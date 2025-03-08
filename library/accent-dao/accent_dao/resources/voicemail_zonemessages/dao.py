# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import daosession

from .persistor import VoicemailZoneMessagesPersistor


@daosession
def find_all(session):
    return VoicemailZoneMessagesPersistor(session).find_all()


@daosession
def edit_all(session, voicemail_zonemessages):
    VoicemailZoneMessagesPersistor(session).edit_all(voicemail_zonemessages)
