# accent_auth/services/all_users.py

import logging
from collections import defaultdict

# from accent_auth.database.helpers import commit_or_rollback  # REMOVED
from accent_auth.db import DAO
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AllUsersService:
    def __init__(self, dao: DAO, all_users_policies: dict[str, bool]):
        self._dao = dao
        self._all_users_policies = all_users_policies

    async def update_policies(
        self, tenant_uuids: list[str], session: AsyncSession
    ) -> None:
        logger.debug(
            "all_users: found %s policies to apply to all users of %s tenants",
            len(self._all_users_policies),
            len(tenant_uuids),
        )
        existing_config_managed_policies_by_tenant: dict[str, list] = defaultdict(list)
        for policy in await self._dao.policy.list_(read_only=True, session=session):
            existing_config_managed_policies_by_tenant.setdefault(
                policy.tenant_uuid, []
            ).append(policy)

        policies = await self.find_policies(session=session)
        current_group_policy_associations = (
            await self._dao.group_policy.get_all_policy_associations(session=session)
        )
        for tenant_uuid in tenant_uuids:
            await self.associate_policies_for_tenant(
                tenant_uuid,
                policies,
                current_group_policy_associations,
                existing_config_managed_policies_by_tenant,
                session=session,
            )

        # commit_or_rollback()  # REMOVED - Handled by lifespan/get_db

    async def find_policies(self, session: AsyncSession) -> list:
        policies = []
        for slug, enabled in self._all_users_policies.items():
            if not enabled:
                logger.debug("all_users: policy disabled: %s", slug)
                continue

            policy = await self._dao.policy.find_by(slug=slug, session=session)
            if not policy:
                logger.error("all_users: Unable to found policy: %s", slug)
                continue
            policies.append(policy)

        return policies

    async def associate_policies_for_tenant(
        self,
        tenant_uuid: str,
        policies: list,
        current_group_policy_associations: set[tuple[str, str]],
        existing_config_managed_policies_by_tenant: dict[str, list],
        session: AsyncSession,
    ) -> None:
        all_users_group = await self._dao.group.get_all_users_group(
            tenant_uuid, session=session
        )
        for policy in policies:
            if (all_users_group.uuid, policy.uuid) in current_group_policy_associations:
                continue
            await self._associate_policy(
                tenant_uuid, policy.uuid, all_users_group.uuid, session=session
            )
            current_group_policy_associations.add((all_users_group.uuid, policy.uuid))

        existing_config_managed_policies = (
            existing_config_managed_policies_by_tenant.get(tenant_uuid) or []
        )
        policies_to_dissociate = [
            policy
            for policy in existing_config_managed_policies
            if policy.config_managed and policy.slug not in self._all_users_policies
        ]
        for policy in policies_to_dissociate:
            await self._dissociate_policy(
                tenant_uuid, policy.uuid, all_users_group.uuid, session=session
            )

    async def _associate_policy(
        self, tenant_uuid: str, policy_uuid: str, group_uuid: str, session: AsyncSession
    ) -> None:
        logger.debug(
            "all_users: tenant %s: associating policy %s to group %s",
            tenant_uuid,
            policy_uuid,
            group_uuid,
        )
        await self._dao.group_policy.create(
            group_uuid=group_uuid, policy_uuid=policy_uuid, session=session
        )

    async def _dissociate_policy(
        self, tenant_uuid: str, policy_uuid: str, group_uuid: str, session: AsyncSession
    ) -> None:
        logger.debug(
            "all_users: tenant %s: dissociating policy %s from group %s",
            tenant_uuid,
            policy_uuid,
            group_uuid,
        )
        await self._dao.group_policy.delete(
            group_uuid=group_uuid, policy_uuid=policy_uuid, session=session
        )
