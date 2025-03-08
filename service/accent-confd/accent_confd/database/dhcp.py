# Copyright 2023 Accent Communications

from accent_dao.alchemy.dhcp import Dhcp
from accent_dao.helpers.db_manager import Session


def get():
    return Session.query(Dhcp).first()


def update(dhcp_form):
    dhcp = Session.query(Dhcp).first()
    for name, value in dhcp_form.items():
        setattr(dhcp, name, value)
