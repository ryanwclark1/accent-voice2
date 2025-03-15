# src/accent_chatd/dao/tenant.py


from sqlalchemy import select

from accent_chatd.exceptions import UnknownTenantException
from accent_chatd.models import Tenant

from .base import BaseDAO


class TenantDAO(BaseDAO):
    async def get(self, tenant_uuid: str) -> Tenant:
        async with self.session() as session:
            result = await session.execute(
                select(Tenant).where(Tenant.uuid == tenant_uuid)
            )
            tenant = result.scalars().first()
            if not tenant:
                raise UnknownTenantException(tenant_uuid)
            return tenant

    async def list_(self) -> list[Tenant]:
        async with self.session() as session:
            result = await session.execute(select(Tenant))
            return result.scalars().all()

    async def create(self, tenant: Tenant) -> Tenant:
        async with self.session() as session:
            async with session.begin():
                session.add(tenant)
                await session.flush()
                await session.refresh(tenant)  # Refresh to load generated fields.
                return tenant

    async def find_or_create(self, tenant_uuid: str) -> Tenant:
        try:
            return await self.get(tenant_uuid)
        except UnknownTenantException:
            return await self.create(Tenant(uuid=tenant_uuid))

    async def delete(self, tenant: Tenant) -> None:
        async with self.session() as session:
            async with session.begin():
                await session.delete(tenant)
