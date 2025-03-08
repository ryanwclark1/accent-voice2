# accent_auth/services/default_group.py

import logging

# from accent_auth.database.helpers import commit_or_rollback  # REMOVED
from accent_auth.db import DAO
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class DefaultGroupService:
    def __init__(self, dao: DAO, default_groups: dict):
        self._dao = dao
        self._default_groups = default_groups

    async def update_groups(
        self, tenant_uuids: list[str], session: AsyncSession
    ) -> None:
        logger.debug(
            "Found %s groups to apply in every tenant",
            len(self._default_groups),
        )
        groups = await self._dao.group.find_all_by(
            slug=list(self._default_groups.keys()), session=session
        )
        group_by_slug_tenant = {
            (group.slug, group.tenant_uuid): group for group in groups
        }
        policies = await self._dao.policy.list_(session=session)
        policies_by_group: dict[str, list] = {}
        for policy in policies:
            for group in policy.groups:  # type: ignore
                if group.uuid not in policies_by_group:
                    policies_by_group[group.uuid] = []
                policies_by_group[group.uuid].append(policy.slug)

        for tenant_uuid in tenant_uuids:
            await self.update_groups_for_tenant(
                tenant_uuid, group_by_slug_tenant, policies_by_group, session=session
            )
        # commit_or_rollback() # Removed

    async def create_groups_for_new_tenant(
        self, tenant_uuid: str, session: AsyncSession
    ) -> None:
        await self.update_groups_for_tenant(tenant_uuid, {}, {}, session=session)

    async def update_groups_for_tenant(
        self,
        tenant_uuid: str,
        group_by_slug_tenant: dict,
        policies_by_group: dict,
        session: AsyncSession,
    ) -> None:
        for group_slug, group_args in self._default_groups.items():
            group = group_by_slug_tenant.get((group_slug, tenant_uuid))
            if group:
                await self._update_group(
                    tenant_uuid,
                    group.uuid,
                    group_slug,
                    group_args,
                    policies_by_group,
                    session=session,
                )
            else:
                await self._create_group(
                    tenant_uuid, group_slug, group_args, session=session
                )

    async def _create_group(
        self, tenant_uuid: str, group_slug: str, group: dict, session: AsyncSession
    ) -> None:
        logger.debug("Tenant %s: creating group %s", tenant_uuid, group_slug)
        group = dict(group)  # Create a copy to avoid modifying the original
        policies = group.pop("policies", {})
        group_uuid = await self._dao.group.create(
            name=group_slug,
            slug=group_slug,
            tenant_uuid=tenant_uuid,
            system_managed=True,
            session=session,
            **group,
        )
        enabled_policies = (
            policy_slug for policy_slug, enabled in policies.items() if enabled
        )
        for policy_slug in enabled_policies:
            logger.debug(
                "Tenant %s: adding policy %s to group %s",
                tenant_uuid,
                policy_slug,
                group_slug,
            )
            policy = await self._dao.policy.find_by(slug=policy_slug, session=session)
            if not policy:
                logger.error(
                    'Tenant %s: Policy "%s" does not exist. '
                    'Skipping association with default group "%s"',
                    tenant_uuid,
                    policy_slug,
                    group_slug,
                )
                continue
            await self._dao.group_policy.create(
                group_uuid=group_uuid, policy_uuid=policy.uuid, session=session
            )  # Use the new relationship

    async def _update_group(
        self,
        tenant_uuid: str,
        group_uuid: str,
        group_slug: str,
        group: dict,
        policies_by_group: dict,
        session: AsyncSession,
    ) -> None:
        logger.debug("Tenant %s: updating group %s", tenant_uuid, group_slug)
        group = dict(group)  # Create a copy
        policies = group.pop("policies", {})
        await self._dao.group.update(
            group_uuid,
            session=session,
            name=group_slug,
            **group,
        )

        enabled_policies = (
            policy_slug for policy_slug, enabled in policies.items() if enabled
        )
        disabled_policies = (
            policy_slug for policy_slug, enabled in policies.items() if not enabled
        )
        existing_policies = set(policies_by_group.get(group_uuid) or [])
        policies_to_add = set(enabled_policies) - set(existing_policies)
        policies_to_remove = set(disabled_policies) & set(existing_policies)

        for policy_slug in policies_to_add:
            logger.debug(
                "Tenant %s: adding policy %s to group %s",
                tenant_uuid,
                policy_slug,
                group_slug,
            )
            policy = await self._dao.policy.find_by(slug=policy_slug, session=session)
            if not policy:
                logger.error(
                    'Tenant %s: Policy "%s" does not exist. '
                    'Skipping association with default group "%s"',
                    tenant_uuid,
                    policy_slug,
                    group_slug,
                )
                continue
            await self._dao.group_policy.create(
                group_uuid=group_uuid, policy_uuid=policy.uuid, session=session
            )  # Use the new relationship

        for policy_slug in policies_to_remove:
            logger.debug(
                "Tenant %s: removing policy %s from group %s",
                tenant_uuid,
                policy_slug,
                group_slug,
            )
            policy = await self._dao.policy.find_by(slug=policy_slug, session=session)
            if not policy:
                logger.error(
                    'Tenant %s: Policy "%s" does not exist. '
                    'Skipping dissociation with default group "%s"',
                    tenant_uuid,
                    policy_slug,
                    group_slug,
                )
                continue
            await self._dao.group_policy.delete(
                group_uuid=group_uuid, policy_uuid=policy.uuid, session=session
            )  # Use the new relationship
