# Copyright 2023 Accent Communications


from ...exceptions import ExportNotFoundException
from ..models import Export
from .base import BaseDAO


class _UselessQuery(Exception):
    pass


class ExportDAO(BaseDAO):
    def get(self, export_uuid, tenant_uuids=None):
        with self.new_session() as session:
            query = session.query(Export)
            try:
                query = self._apply_filters(query, {'tenant_uuids': tenant_uuids})
            except _UselessQuery:
                raise ExportNotFoundException(export_uuid)

            query = query.filter(Export.uuid == export_uuid)
            export = query.one_or_none()
            if not export:
                raise ExportNotFoundException(export_uuid)
            session.expunge_all()
            return export

    def _add_tenant_filter(self, query, tenant_uuids):
        if tenant_uuids:
            query = query.filter(Export.tenant_uuid.in_(tenant_uuids))
        elif not tenant_uuids and tenant_uuids is not None:
            raise _UselessQuery()
        return query

    def _apply_filters(self, query, params):
        query = self._add_tenant_filter(query, params.get('tenant_uuids'))
        return query

    def create(self, export):
        with self.new_session() as session:
            session.add(export)
            session.flush()
            session.expunge(export)
        return export

    def update(self, export):
        with self.new_session() as session:
            session.add(export)
            session.flush()
            session.expunge(export)
