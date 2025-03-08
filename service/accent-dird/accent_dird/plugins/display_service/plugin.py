# Copyright 2023 Accent Communications

import logging

from accent_dird import BaseServicePlugin, database
from accent_dird.database.helpers import Session

logger = logging.getLogger(__name__)


class DisplayServicePlugin(BaseServicePlugin):
    def load(self, dependencies):
        return _DisplayService(database.DisplayCRUD(Session))


class _DisplayService:
    def __init__(self, crud):
        self._display_crud = crud

    def count(self, visible_tenants, **list_params):
        return self._display_crud.count(visible_tenants, **list_params)

    def create(self, **body):
        return self._display_crud.create(**body)

    def delete(self, display_uuid, visible_tenants):
        return self._display_crud.delete(visible_tenants, display_uuid)

    def edit(self, display_uuid, visible_tenants, **body):
        return self._display_crud.edit(visible_tenants, display_uuid, **body)

    def get(self, display_uuid, visible_tenants):
        return self._display_crud.get(visible_tenants, display_uuid)

    def list_(self, visible_tenants, **list_params):
        return self._display_crud.list_(visible_tenants, **list_params)
