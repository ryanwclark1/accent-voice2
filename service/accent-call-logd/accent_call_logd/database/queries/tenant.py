# Copyright 2023 Accent Communications

from ..models import Tenant
from .base import BaseDAO


class TenantDAO(BaseDAO):
    def create_all_uuids_if_not_exist(self, tenant_uuids):
        with self.new_session() as session:
            for tenant_uuid in tenant_uuids:
                if session.query(Tenant).get(tenant_uuid):
                    continue

                tenant = Tenant(uuid=tenant_uuid)
                session.add(tenant)
                session.flush()
