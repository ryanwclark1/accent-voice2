# Copyright 2023 Accent Communications

from accent_dao.alchemy.mail import Mail
from accent_dao.helpers.db_manager import Session


def get():
    return Session.query(Mail).first()


def update(email_config):
    Session.add(email_config)
    Session.flush()
