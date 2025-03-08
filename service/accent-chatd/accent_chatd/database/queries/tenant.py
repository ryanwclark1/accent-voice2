# Copyright 2023 Accent Communications

from ...exceptions import UnknownTenantException
from ..models import Tenant


class TenantDAO:
    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session()

    def get(self, tenant_uuid):
        tenant = self.session.query(Tenant).get(tenant_uuid)
        if not tenant:
            raise UnknownTenantException(tenant_uuid)
        return tenant

    def list_(self):
        return self.session.query(Tenant).all()

    def create(self, tenant):
        self.session.add(tenant)
        self.session.flush()
        return tenant

    def find_or_create(self, tenant_uuid):
        result = self.session.query(Tenant).get(tenant_uuid)
        if result:
            return result

        tenant = Tenant(uuid=tenant_uuid)
        return self.create(tenant)

    def delete(self, tenant):
        self.session.delete(tenant)
        self.session.flush()
