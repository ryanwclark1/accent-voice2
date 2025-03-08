# accent_auth/services/default_policy.py

import logging

# from accent_auth.database.helpers import commit_or_rollback  # REMOVED
from accent_auth.db import DAO
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class DefaultPolicyService:
    def __init__(self, dao: DAO, default_policies: dict[str, dict]):
        self._dao = dao
        self._default_policies = default_policies

    async def update_policies(
        self, top_tenant_uuid: str, session: AsyncSession
    ) -> None:
        logger.debug(
            "default_policies: found %s policies to apply",
            len(self._default_policies),
        )
        await self.update_policies_for_tenant(top_tenant_uuid, session=session)
        # commit_or_rollback() # Removed

    async def update_policies_for_tenant(
        self, tenant_uuid: str, session: AsyncSession
    ) -> None:
        for slug, policy_args in self._default_policies.items():
            policy = await self._dao.policy.find_by(
                slug=slug, tenant_uuid=tenant_uuid, session=session
            )
            if policy:
                await self._update_policy(
                    policy.uuid, slug, policy_args, session=session
                )
            else:
                await self._create_policy(
                    tenant_uuid, slug, policy_args, session=session
                )

    async def delete_orphan_policies(self, session: AsyncSession) -> None:
        policies = await self._dao.policy.list_(read_only=True, session=session)
        for policy in policies:
            if policy.slug not in self._default_policies:
                await self._delete_policy(policy.uuid, session=session)
        # commit_or_rollback() # Removed

    async def _create_policy(
        self, tenant_uuid: str, slug: str, policy: dict, session: AsyncSession
    ) -> None:
        logger.debug("default_policies: creating policy %s", slug)
        policy.setdefault("description", "Automatically created")
        await self._dao.policy.create(
            name=slug,
            slug=slug,
            tenant_uuid=tenant_uuid,
            config_managed=True,
            shared=False,  # Ensure shared is set, as per your requirements
            session=session,
            **policy,
        )

    async def _update_policy(
        self, policy_uuid: str, policy_slug: str, policy: dict, session: AsyncSession
    ) -> None:
        logger.debug("default_policies: updating policy %s", policy_uuid)
        policy.setdefault("description", "Automatically created")
        await self._dao.policy.update(
            policy_uuid,
            session=session,
            name=policy_slug,
            config_managed=True,
            shared=policy.get("shared", False),
            **policy,
        )

    async def _delete_policy(self, policy_uuid: str, session: AsyncSession) -> None:
        if await self._dao.policy.is_associated(policy_uuid, session=session):
            logger.warning(
                "default_policies: deleting policy %s (SKIPPED: associated)",
                policy_uuid,
            )
            return

        logger.debug("default_policies: deleting policy %s", policy_uuid)
        await self._dao.policy.delete(policy_uuid, session=session)
