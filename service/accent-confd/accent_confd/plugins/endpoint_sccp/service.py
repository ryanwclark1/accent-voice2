# Copyright 2023 Accent Communications

from accent_dao.resources.endpoint_sccp import dao

from accent_confd.helpers.resource import CRUDService

from .notifier import build_notifier
from .validator import build_validator


class SccpEndpointService(CRUDService):
    pass


def build_service():
    return SccpEndpointService(dao, build_validator(), build_notifier())
