# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import daosession

from .persistor import QueueGeneralPersistor


@daosession
def find_all(session):
    return QueueGeneralPersistor(session).find_all()


@daosession
def edit_all(session, queue_general):
    QueueGeneralPersistor(session).edit_all(queue_general)
