# Copyright 2023 Accent Communications

from accent_dao.resources.switchboard import dao as switchboard_dao

from accent_confd.helpers.resource import CRUDService
from accent_confd.helpers.validator import ValidationGroup

from .notifier import build_notifier


def build_service():
    return CRUDService(switchboard_dao, ValidationGroup(), build_notifier())
