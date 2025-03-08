# Copyright 2023 Accent Communications

from accent_dao.resources.meeting import dao

from accent_confd.helpers.resource import CRUDService

from .validator import build_validator


def build_service(notifier):
    return CRUDService(dao, build_validator(), notifier)
