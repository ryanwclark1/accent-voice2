# Copyright 2023 Accent Communications
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from accent_call_logd.database.models import Export
    from accent_call_logd.database.queries import DAO


class ExportService:
    def __init__(self, dao: DAO) -> None:
        self._dao = dao

    def get(self, export_uuid: str, tenant_uuids: list[str]) -> Export:
        return self._dao.export.get(export_uuid, tenant_uuids)

    def create(self, *args: Any, **kwargs: Any) -> Export:
        return self._dao.export.create(*args, **kwargs)

    def update(self, export: Export) -> None:
        self._dao.export.update(export)
