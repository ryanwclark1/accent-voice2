# Copyright 2023 Accent Communications

from sqlalchemy.exc import IntegrityError

from accent_dao.alchemy.tenant import Tenant
from accent_dao.helpers.db_manager import daosession


@daosession
def find_or_create_tenant(session, tenant_uuid):
    tenant = session.query(Tenant).get(tenant_uuid)

    if tenant:
        return tenant

    tenant = Tenant(uuid=tenant_uuid)

    session.begin_nested()
    try:
        session.add(tenant)
        session.commit()
    except IntegrityError:
        session.rollback()
        tenant = session.query(Tenant).get(tenant_uuid)
    return tenant


@daosession
def find(session):
    return session.query(Tenant).first()
