# Copyright 2023 Accent Communications

from accent_dao.resources.incall import dao as incall_dao
from accent_dao.resources.incall import strategy

from accent_confd.helpers.resource import CRUDService

from .notifier import build_notifier
from .validator import build_validator


class IncallService(CRUDService):
    @incall_dao.query_options(*strategy.incall_preload_relationships)
    def get(self, resource_id, **kwargs):
        return super().get(resource_id, **kwargs)

    @incall_dao.query_options(*strategy.incall_preload_relationships)
    def search(self, parameters, tenant_uuids=None):
        return super().search(parameters, tenant_uuids)


def build_service():
    return IncallService(incall_dao, build_validator(), build_notifier())
