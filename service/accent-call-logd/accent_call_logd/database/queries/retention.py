# Copyright 2023 Accent Communications

import logging

from ..models import Config, Retention, Tenant
from .base import BaseDAO

logger = logging.getLogger(__name__)


class RetentionDAO(BaseDAO):
    def find(self, tenant_uuid):
        with self.new_session() as session:
            query = session.query(Retention)
            query = query.filter(Retention.tenant_uuid == tenant_uuid)
            retention = query.first()
            if not retention:
                retention = Retention(tenant_uuid=tenant_uuid)
            else:
                session.flush()
                session.expunge(retention)
            config = session.query(Config).first()
            retention.default_cdr_days = config.retention_cdr_days
            retention.default_export_days = config.retention_export_days
            retention.default_recording_days = config.retention_recording_days
        return retention

    def find_or_create(self, tenant_uuid):
        with self.new_session() as session:
            query = session.query(Retention)
            query = query.filter(Retention.tenant_uuid == tenant_uuid)
            retention = query.first()
            if not retention:
                tenant = self._find_or_create_tenant(session, tenant_uuid)
                retention = Retention(tenant_uuid=tenant.uuid)
                session.add(retention)
            config = session.query(Config).first()
            retention.default_cdr_days = config.retention_cdr_days
            retention.default_export_days = config.retention_export_days
            retention.default_recording_days = config.retention_recording_days
            session.flush()
            session.expunge(retention)
        return retention

    def _find_or_create_tenant(self, session, tenant_uuid):
        tenant = session.query(Tenant).get(tenant_uuid)
        if not tenant:
            tenant = Tenant(uuid=tenant_uuid)
            session.add(tenant)
            session.flush()
        return tenant

    def update(self, retention):
        with self.new_session() as session:
            session.add(retention)
            session.flush()
            session.expunge(retention)

    def delete(self, tenant_uuid):
        with self.new_session() as session:
            deleted_count = (
                session.query(Retention)
                .filter(Retention.tenant_uuid == tenant_uuid)
                .delete()
            )
            logger.debug(
                "Deleted %d Retention entries for tenant_uuid %s",
                deleted_count,
                tenant_uuid,
            )
