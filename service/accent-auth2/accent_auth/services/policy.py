# accent_auth/services/policy.py

from typing import Any

from accent_auth.db import DAO
from accent_auth import exceptions
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Policy, PolicyAccess, Access, Tenant, UserPolicy, GroupPolicy
from sqlalchemy import and_, or_, text


class PolicyService:  # No longer inherits from BaseService
    def __init__(self, dao: DAO):
        self._dao = dao

    async def add_access(
        self, policy_uuid: str, access: str, db: AsyncSession = None
    ) -> None:
        await self._dao.policy_access.create(
            policy_uuid=policy_uuid, access=access, session=db
        )

    async def create(
        self, db: AsyncSession = None, **kwargs
    ) -> str:  # Added the missing parameters
        return await self._dao.policy.create(session=db, **kwargs)

    async def count(
        self, db: AsyncSession, **kwargs
    ) -> int:  # Added the missing parameters
        return await self._dao.policy.count(session=db, **kwargs)

    async def delete(
        self, policy_uuid: str, db: AsyncSession = None, tenant_uuids: list = None
    ) -> None:
        return await self._dao.policy.delete(policy_uuid, session=db)

    async def delete_access(
        self, policy_uuid: str, access: str, db: AsyncSession = None
    ) -> None:
        await self._dao.policy_access.delete(
            policy_uuid=policy_uuid, access=access, session=db
        )

    async def exists(
        self,
        policy_uuid: str,
        db: AsyncSession = None,
        tenant_uuids: list[str] | None = None,
    ) -> bool:
        return await self._dao.policy.exists(
            policy_uuid, session=db, tenant_uuids=tenant_uuids
        )

    async def _is_associated_user(self, uuid: str, db: AsyncSession = None):
        return await self._dao.user_policy.count(policy_uuid=uuid, session=db) > 0

    async def _is_associated_group(self, uuid, db: AsyncSession = None):
        return await self._dao.group_policy.count(policy_uuid=uuid, session=db) > 0

    async def is_associated(self, uuid: str, db: AsyncSession = None) -> bool:
        return await self._is_associated_user(
            uuid, db=db
        ) or await self._is_associated_group(uuid, db=db)

    async def get(
        self, policy_uuid: str, db: AsyncSession, tenant_uuids: list | None = None
    ) -> Policy:
        return await self._dao.policy.get(
            policy_uuid, session=db, tenant_uuids=tenant_uuids
        )

    async def get_by_slug(
        self, policy_slug: str, db: AsyncSession, tenant_uuids: list[str] | None = None
    ) -> Policy:
        return await self._dao.policy.get_by(
            slug=policy_slug, session=db, tenant_uuids=tenant_uuids
        )

    async def list_(self, db: AsyncSession, tenant_uuids=None, **kwargs) -> list:
        return await self._dao.policy.list_(
            session=db, tenant_uuids=tenant_uuids, **kwargs
        )

    async def update(self, policy_uuid, db: AsyncSession, **kwargs) -> dict:
        return await self._dao.policy.update(policy_uuid, session=db, **kwargs)
