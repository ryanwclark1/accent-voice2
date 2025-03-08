# Copyright 2023 Accent Communications

from accent_dao.resources.tenant import dao

from accent_confd.helpers.resource import CRUDService


def build_service():
    return CRUDService(dao, None, None)
