# accent_auth/tenants/service.py

import logging

# from accent_auth.services.helpers import BaseService  # REMOVED
from accent_auth.db import DAO
from accent_auth import exceptions
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class TenantService:  # Removed inheritance
    def __init__(
        self,
        dao: DAO,
        all_users_policies,
        default_group_service,
        bus_publisher=None,
    ):
        # super().__init__(dao)  # REMOVED
        self._dao: DAO = dao
        self._bus_publisher = bus_publisher
        self._all_users_policies = all_users_policies
        self._default_group_service = default_group_service

    async def count(self, scoping_tenant_uuid, db: AsyncSession, **kwargs):
        return await self._dao.tenant.count(
            scoping_tenant_uuid=scoping_tenant_uuid, session=db, **kwargs
        )  # Added session

    async def create(self, db: AsyncSession, **kwargs):
        async with db.begin_nested():  # Use a nested transaction
            uuid = await self._dao.tenant.create(session=db, **kwargs)
            await self._dao.address.create(
                tenant_uuid=uuid, session=db, **kwargs["address"]
            )
            result = await self._get(uuid, db=db)

            # event = TenantCreatedEvent(
            #     {
            #         'uuid': uuid,
            #         'name': result['name'],
            #         'slug': result['slug'],
            #         'domain_names': result['domain_names'],
            #     },
            #     uuid,
            # )
            # self._bus_publisher.publish(event)

            name = f"accent-all-users-tenant-{uuid}"
            all_users_group_uuid = await self._dao.group.create(
                name=name,
                slug=name,
                tenant_uuid=uuid,
                system_managed=True,
                session=db,
            )
            for slug, enabled in self._all_users_policies.items():
                if not enabled:
                    continue

                all_users_policy = await self._dao.policy.find_by(slug=slug, session=db)
                if not all_users_policy:
                    raise Exception("All users policy %s not found" % slug)
                await self._dao.group_policy.create(
                    group_uuid=all_users_group_uuid,
                    policy_uuid=all_users_policy.uuid,
                    session=db,
                )  # Added session
            await self._default_group_service.create_groups_for_new_tenant(
                uuid, session=db
            )
            await db.flush()  # Added flush
            return result

    async def find_top_tenant(self, db: AsyncSession):
        return await self._dao.tenant.get_top_tenant(session=db)  # Use DAO

    async def delete(self, scoping_tenant_uuid, tenant_uuid, db: AsyncSession):
        visible_tenants = await self.list_sub_tenants(scoping_tenant_uuid, db=db)
        if str(tenant_uuid) not in visible_tenants:
            raise exceptions.UnknownTenantException(tenant_uuid)

        await self._dao.tenant.delete(tenant_uuid, session=db)  # Added session

        # event = TenantDeletedEvent(tenant_uuid)  # Removed event, needs refactoring.
        # self._bus_publisher.publish(event)

    async def get(self, scoping_tenant_uuid, tenant_uuid, db: AsyncSession):
        visible_tenants = await self.list_sub_tenants(scoping_tenant_uuid, db=db)
        if str(tenant_uuid) not in visible_tenants:
            raise exceptions.UnknownTenantException(tenant_uuid)
        return await self._get(tenant_uuid, db=db)

    async def _get(self, tenant_uuid, db: AsyncSession):
        tenants = await self._dao.tenant.get(
            tenant_uuid, session=db
        )  # Added session and limit
        for tenant in tenants:
            return tenant
        raise exceptions.UnknownTenantException(tenant_uuid)

    async def get_by_uuid_or_slug(
        self, scoping_tenant_uuid, id_, db: AsyncSession
    ):  # Added session
        visible_tenants = await self._dao.tenant.list_visible_tenants(
            scoping_tenant_uuid, session=db
        )
        for tenant in visible_tenants:
            if tenant.uuid == id_ or tenant.slug == id_:
                return await self._get(tenant.uuid, db=db)

        raise exceptions.UnknownTenantException(id_)

    async def list_(self, scoping_tenant_uuid, db: AsyncSession, **kwargs):
        return await self._dao.tenant.list_(
            scoping_tenant_uuid=scoping_tenant_uuid, session=db, **kwargs
        )  # Pass session

    async def list_sub_tenants(self, tenant_uuid: str, db: AsyncSession) -> list[str]:
        visible_tenants = await self._dao.tenant.list_visible_tenants(
            tenant_uuid, session=db
        )
        return [tenant.uuid for tenant in visible_tenants]

    async def update(
        self, scoping_tenant_uuid, tenant_uuid, db: AsyncSession, **kwargs
    ):
        visible_tenants = await self.list_sub_tenants(scoping_tenant_uuid, db=db)

        if str(tenant_uuid) not in visible_tenants:
            raise exceptions.UnknownTenantException(tenant_uuid)
        address_id = await self._dao.tenant.get_address_id(tenant_uuid, session=db)
        if not address_id:
            address_id = self._dao.address.new(
                tenant_uuid=tenant_uuid, session=db, **kwargs["address"]
            )
        else:
            address_id = self._dao.address.update(
                address_id, session=db, **kwargs["address"]
            )

        await self._dao.tenant.update(tenant_uuid, session=db, **kwargs)  # Pass session
        result = await self._get(tenant_uuid, db=db)
        # event = TenantUpdatedEvent(result.get('name'), tenant_uuid)  #Removed as it needs refactoring.
        # self._bus_publisher.publish(event)
        return result

    async def list_domains(self, tenant_uuid, db: AsyncSession):
        if await self.get(tenant_uuid, tenant_uuid, db=db) is None:
            raise exceptions.UnknownTenantException(tenant_uuid)

        domains = await self._dao.domain.get(str(tenant_uuid), session=db)
        return [{"name": domain.name, "uuid": domain.uuid} for domain in domains]
