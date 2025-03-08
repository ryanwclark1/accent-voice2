# Copyright 2023 Accent Communications

from accent_dao.resources.outcall import dao as outcall_dao

from accent_confd.helpers.resource import CRUDService

from .notifier import build_notifier
from .validator import build_validator


def build_service():
    return CRUDService(outcall_dao, build_validator(), build_notifier())
