# accent_auth/groups/service.py

from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db import DAO
from accent_auth import exceptions
from .models import Group


class GroupService:  # Removed BaseService inheritance
    def __init__(self, dao: DAO):
        self._dao = dao

    async def add_policy(
        self, group_uuid: str, policy_uuid: str, db: AsyncSession
    ) -> None:
        """Adds a policy to a group."""
        try:
            await self._dao.group_policy.create(
                group_uuid=group_uuid, policy_uuid=policy_uuid, session=db
            )
        except Exception as e:  # This needs to be more specific
            raise e

    async def add_user(self, group_uuid: str, user_uuid: str, db: AsyncSession) -> None:
        """Adds a user to a group."""
        if await self._dao.group.is_system_managed(group_uuid, session=db):
            raise exceptions.SystemGroupForbidden(group_uuid)
        try:
            await self._dao.user_group.create(
                user_uuid=user_uuid, group_uuid=group_uuid, session=db
            )
        except Exception as e:  # This needs to be more specific
            raise e

    async def count(self, db: AsyncSession, **kwargs) -> int:
        """Counts the number of groups."""
        return await self._dao.group.count(session=db, **kwargs)

    async def count_policies(self, group_uuid: str, db: AsyncSession, **kwargs) -> int:
        """Counts the number of policies associated with a group."""
        return await self._dao.group_policy.count(
            group_uuid=group_uuid, session=db, **kwargs
        )

    async def count_users(self, group_uuid: str, db: AsyncSession, **kwargs) -> int:
        """Counts the number of users in a group."""
        return await self._dao.user_group.count(
            group_uuid=group_uuid, session=db, **kwargs
        )

    async def create(self, db: AsyncSession, **kwargs) -> dict:
        """Creates a new group."""
        kwargs.setdefault("system_managed", False)
        if not kwargs.get("slug"):
            pass  # TODO: Generate a slug
        group = await self._dao.group.create(session=db, **kwargs)
        return group

    async def delete(
        self, group_uuid: str, db: AsyncSession, tenant_uuids: list[str] | None = None
    ) -> None:
        """Deletes a group."""
        if await self._dao.group.is_system_managed(
            group_uuid, session=db, tenant_uuids=tenant_uuids
        ):
            raise exceptions.SystemGroupForbidden(group_uuid)
        return await self._dao.group.delete(
            group_uuid, session=db, tenant_uuids=tenant_uuids
        )

    async def exists(
        self, uuid: str, db: AsyncSession, tenant_uuids: list[str] | None = None
    ) -> bool:
        return await self._dao.group.exists(uuid, session=db, tenant_uuids=tenant_uuids)

    async def find_by(self, db: AsyncSession, **kwargs):
        return await self._dao.group.find_by(session=db, **kwargs)

    async def get(
        self, group_uuid: str, db: AsyncSession, tenant_uuids: list[str] | None = None
    ) -> dict:
        """Gets a group by UUID."""
        group = await self._dao.group.get(
            group_uuid, session=db, tenant_uuids=tenant_uuids
        )
        if not group:
            raise exceptions.UnknownGroupException(group_uuid)
        return group

    async def get_all_policy_associations(self, db: AsyncSession):
        result = await self._dao.group_policy.get_all_policy_associations(session=db)
        return {(row.group_uuid, row.policy_uuid) for row in result}

    async def get_acl(self, user_uuid: str, db: AsyncSession) -> list[str]:
        """Compiles the complete ACL for a user based on group memberships."""
        groups = await self._dao.group.list_(user_uuid=user_uuid, session=db)
        acl = []
        for group in groups:
            policies = await self.list_policies(
                group["uuid"], db=db
            )  # No circular import
            for policy in policies:
                acl.extend(policy.acl)
        return acl

    async def list_(self, db: AsyncSession, **kwargs) -> list:
        """Lists groups, applying filters and pagination."""
        return await self._dao.group.list_(session=db, **kwargs)

    async def update(self, group_uuid, db: AsyncSession, **kwargs) -> dict:
        """Updates a group."""
        if await self._dao.group.is_system_managed(group_uuid, session=db):
            raise exceptions.SystemGroupForbidden(group_uuid)

        await self._dao.group.update(group_uuid, session=db, **kwargs)
        return await self._dao.group.get(group_uuid, session=db)  # Use get

    async def remove_policy(
        self, group_uuid: str, policy_uuid: str, db: AsyncSession
    ) -> int:
        """Removes a policy from a group."""
        return await self._dao.group_policy.delete(
            policy_uuid=policy_uuid, group_uuid=group_uuid, session=db
        )

    async def remove_user(
        self, group_uuid: str, user_uuid: str, db: AsyncSession
    ) -> int:
        """Removes a user from a group."""
        if await self._dao.group.is_system_managed(group_uuid, session=db):
            raise exceptions.SystemGroupForbidden(group_uuid)
        return await self._dao.user_group.delete(
            user_uuid=user_uuid, group_uuid=group_uuid, session=db
        )

    async def is_system_managed(
        self, uuid: str, db: AsyncSession, tenant_uuids: list[str] | None = None
    ) -> bool:
        return await self._dao.group.is_system_managed(
            uuid, session=db, tenant_uuids=tenant_uuids
        )

    async def list_policies(
        self, group_uuid, db: AsyncSession, **kwargs
    ):  # added to avoid circular import.
        return await self._dao.policy.list_(group_uuid=group_uuid, session=db, **kwargs)

    async def list_users(self, group_uuid, db: AsyncSession, **kwargs):
        return await self._dao.user.list_(
            group_uuid=group_uuid, session=db, **kwargs
        )  # added to avoid circular import

    async def get_all_users_group(self, tenant_uuid, session: AsyncSession):
        name = f"accent-all-users-tenant-{tenant_uuid}"
        return await self._dao.group.find_by(
            name=name, tenant_uuid=tenant_uuid, session=session
        )

    async def assert_group_in_subtenant(self, tenant_uuids, uuid, db: AsyncSession):
        exists = await self._dao.group.exists(
            uuid, tenant_uuids=tenant_uuids, session=db
        )
        if not exists:
            raise exceptions.UnknownGroupException(uuid)
