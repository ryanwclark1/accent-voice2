# Copyright 2023 Accent Communications

from accent_dao.alchemy.provisioning import Provisioning
from accent_dao.helpers.db_manager import Session


def get():
    return Session.query(Provisioning).first()


def update(provisioning_networking):
    Session.add(provisioning_networking)
    Session.flush()
