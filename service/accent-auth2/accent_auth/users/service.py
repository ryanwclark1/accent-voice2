# accent_auth/users/service.py

import logging
from typing import Any

from sqlalchemy import and_, or_, select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db import DAO
from .models import User, Email  # Import from the local models.py
from accent_auth import exceptions
from accent_auth.utils.helpers import (
    PasswordEncrypter,
)  # Assuming you moved PasswordEncrypter

logger = logging.getLogger(__name__)

EXTERNAL_AUTH_METHODS: list[str] = ["saml", "ldap"]


class UserService:
    """Service for user-related operations."""

    def __init__(
        self,
        dao: DAO,
        tenant_service: Any = None,  # Keep type as Any, will be injected.
    ):
        self._dao = dao
        self._tenant_service = (
            tenant_service  # This is optional, and avoids circular dependencies
        )
        self._encrypter = PasswordEncrypter()  # Instantiate here
        self._unknown_user_salt = (
            b"\x00"  # Placeholder. A real system would generate this once.
        )
        self._unknown_user_hash = "invalid"  # Placeholder

    async def add_policy(
        self, user_uuid: str, policy_uuid: str, db: AsyncSession
    ) -> None:
        """Adds a policy to a user."""
        await self._dao.user_policy.create(
            user_uuid=user_uuid, policy_uuid=policy_uuid, session=db
        )

    async def change_password(
        self,
        user_uuid: str,
        old_password: str,
        new_password: str,
        reset: bool = False,
        db: AsyncSession = None,
    ) -> None:
        """Changes the password for a user.

        Args:
            user_uuid: The UUID of the user.
            old_password: The user's current password.
            new_password: The new password to set.
            reset: old password is not validated, used to reset the password.

        Raises:
            AuthenticationFailedException: If the old password is
                incorrect or the user has no password set.
            PasswordIsManagedExternallyException: raised if password cannot
            be updated due to the authentication method.
        """
        user = await self.get_user(user_uuid, db=db)
        login = user["username"]
        if not login:
            login = await self._find_main_email(user, db=db)
        if not login:
            logger.warning("User %s does not have login (username or email)", user_uuid)
            raise exceptions.AuthenticationFailedException()

        if not reset and not await self.verify_password(login, old_password, db=db):
            raise exceptions.AuthenticationFailedException()
        if await self.uses_external_authentication(user, db=db):
            raise exceptions.PasswordIsManagedExternallyException(user["uuid"])

        salt, hash_ = self._encrypter.encrypt_password(new_password)
        await self._dao.user.update(
            user_uuid, session=db, password_salt=salt, password_hash=hash_
        )

    async def _find_main_email(self, user, db: AsyncSession) -> str | None:
        """
        Finds the main and confirmed email of the user.
        Args:
            user: user's data

        Returns: The mail if any or None
        """
        emails = await self._dao.email.list_(user_uuid=user["uuid"], session=db)
        for email in emails:
            if email.main and email.confirmed:
                return email.address
        return None

    async def count_groups(self, user_uuid: str, db: AsyncSession, **kwargs) -> int:
        """Counts the groups associated with a user."""
        return await self._dao.user_group.count(
            user_uuid=user_uuid, session=db, **kwargs
        )

    async def count_sessions(self, user_uuid: str, db: AsyncSession, **kwargs) -> int:
        """Counts the active sessions for a user."""
        return await self._dao.session.count(user_uuid=user_uuid, session=db, **kwargs)

    async def count_policies(self, user_uuid: str, db: AsyncSession, **kwargs) -> int:
        """Counts the policies associated with a user."""
        return await self._dao.user_policy.count(
            user_uuid=user_uuid, session=db, **kwargs
        )

    async def count_users(
        self, scoping_tenant_uuid=None, recurse=False, db: AsyncSession = None, **kwargs
    ) -> int:
        """Counts the number of users based on the provided filters."""
        if scoping_tenant_uuid:
            kwargs["tenant_uuids"] = await self._get_scoped_tenant_uuids(
                scoping_tenant_uuid, recurse, db=db
            )
        return await self._dao.user.count(session=db, **kwargs)

    async def create(self, db: AsyncSession, **kwargs) -> dict[str, Any]:
        """Creates a new user."""
        password = kwargs.pop("password", None)
        # kwargs.setdefault("tenant_uuid", self.top_tenant_uuid)  # Removed top_tenant logic here.
        if password:
            salt, hash_ = self._encrypter.encrypt_password(password)
            kwargs["password_salt"] = salt
            kwargs["password_hash"] = hash_
        username = kwargs["username"]
        if username and await self._dao.user.login_exists(username, session=db):
            raise exceptions.UsernameLoginAlreadyExists(username)

        email = kwargs.get("email_address")
        if email and await self._dao.user.login_exists(email, session=db):
            raise exceptions.EmailLoginAlreadyExists(email)

        user = await self._dao.user.create(session=db, **kwargs)
        return user

    async def delete_password(self, db: AsyncSession, **kwargs):
        search_params = {k: v for k, v in kwargs.items() if v}
        identifier = list(search_params.values())[0]

        logger.debug("removing password for user %s", identifier)
        users = self._dao.user.list_(session=db, limit=1, **search_params)
        if not users:
            raise exceptions.UnknownUserException(identifier, details=kwargs)

        for user in users:
            self._dao.user.change_password(user["uuid"], salt=None, hash_=None)
            return user

    async def delete_user(
        self, scoping_tenant_uuid: str, user_uuid: str, db: AsyncSession
    ) -> None:
        """Deletes a user."""
        await self.assert_user_in_subtenant(scoping_tenant_uuid, user_uuid, db=db)
        await self._dao.user.delete(user_uuid, session=db)

    async def get_user(
        self, user_uuid: str, db: AsyncSession, scoping_tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Gets a user by UUID."""
        if scoping_tenant_uuid:
            await self.assert_user_in_subtenant(scoping_tenant_uuid, user_uuid, db=db)

        user = await self._dao.user.get(user_uuid, session=db)

        if not user:
            raise exceptions.UnknownUserException(user_uuid)
        return user

    async def get_user_uuid_by_login(self, login: str, db: AsyncSession) -> str:
        """Gets a user UUID by login (username or email)."""
        return (await self._dao.user.get_user_by_login(login, session=db)).uuid

    async def get_user_by_login(
        self, login: str, db: AsyncSession
    ) -> User:  # Using the model
        """Gets a user by their login (username or email)."""
        return await self._dao.user.get_user_by_login(login, session=db)

    async def get_credentials(self, user_uuid: str, db: AsyncSession):
        """Get user hash and salt by uuid"""
        return await self._dao.user.get_credentials(user_uuid=user_uuid, session=db)

    async def get_acl(self, user_uuid: str, db: AsyncSession) -> list[str]:
        """Gets the Access Control List (ACL) for a user."""
        user = await self.get_user(user_uuid, db=db)  # Fetch the user
        if not user:
            return []  # Or perhaps raise an exception, depending on your needs

        acl = []
        # Fetch user policies
        user_policies = await self._dao.user_policy.list_(
            user_uuid=user_uuid, session=db
        )
        for user_policy in user_policies:
            policy = await self._dao.policy.get(user_policy.policy_uuid, session=db)
            if policy:
                acl.extend(policy.acl)

        # Fetch policies associated with the user's groups
        user_groups = await self._dao.user_group.list_(user_uuid=user_uuid, session=db)
        for user_group in user_groups:
            group_policies = await self._dao.group_policy.list_(
                group_uuid=user_group.group_uuid, session=db
            )
            for group_policy in group_policies:
                policy = await self._dao.policy.get(
                    group_policy.policy_uuid, session=db
                )
                if policy:
                    acl.extend(policy.acl)
        return acl

    async def get_user_roles(self, user_uuid: str, db: AsyncSession) -> list[str]:
        """Retrieves the roles of a user."""
        user = await self._dao.user.get(user_uuid, session=db)
        if not user:
            raise exceptions.UnknownUserException(user_uuid)
        return user.roles or []

    async def list_groups(self, user_uuid: str, db: AsyncSession, **kwargs) -> list:
        """Lists the groups a user belongs to."""
        return await self._dao.user_group.list_(
            user_uuid=user_uuid, session=db, **kwargs
        )

    async def list_sessions(self, user_uuid: str, db: AsyncSession, **kwargs) -> list:
        """Lists the sessions for a user."""
        return await self._dao.session.list_(user_uuid=user_uuid, session=db, **kwargs)

    async def list_policies(self, user_uuid: str, db: AsyncSession, **kwargs) -> list:
        """Lists the policies associated with a user."""
        return await self._dao.user_policy.list_(
            user_uuid=user_uuid, session=db, **kwargs
        )

    async def list_users(
        self, scoping_tenant_uuid=None, recurse=False, db: AsyncSession = None, **kwargs
    ) -> list:
        """Lists users, potentially filtering by tenant."""
        if scoping_tenant_uuid:
            kwargs["tenant_uuids"] = await self._get_scoped_tenant_uuids(
                scoping_tenant_uuid, recurse, db=db
            )
        return await self._dao.user.list_(session=db, **kwargs)

    async def remove_policy(
        self, user_uuid: str, policy_uuid: str, db: AsyncSession
    ) -> None:
        """Removes a policy from a user."""
        await self._dao.user_policy.delete(
            user_uuid=user_uuid, policy_uuid=policy_uuid, session=db
        )

    async def update(
        self, scoping_tenant_uuid: str, user_uuid: str, db: AsyncSession, **kwargs
    ) -> dict:
        """Updates a user's information."""
        await self.assert_user_in_subtenant(scoping_tenant_uuid, user_uuid, db=db)
        username = kwargs["username"]
        if username and await self._dao.user.login_exists(
            username, ignored_user=user_uuid, session=db
        ):
            raise exceptions.UsernameLoginAlreadyExists(username)

        await self._dao.user.update(user_uuid, session=db, **kwargs)
        return await self.get_user(user_uuid, db=db)

    async def update_emails(self, user_uuid, emails, db: AsyncSession):
        return await self._dao.user.update_emails(user_uuid, emails, session=db)

    async def verify_password(
        self, login: str, password: str, reset: bool = False, db: AsyncSession = None
    ) -> bool:
        """Verifies a user's password."""

        if reset:
            return True

        try:
            user = await self._dao.user.get_user_by_login(login, session=db)
            hash_ = user.password_hash
            salt = user.password_salt
        except exceptions.UnknownLoginException:
            hash_ = self._unknown_user_hash
            salt = self._unknown_user_salt

        if not hash_ or not salt:
            hash_ = self._unknown_user_hash
            salt = self._unknown_user_salt

        return hash_ == self._encrypter.compute_password_hash(password, salt)

    async def uses_external_authentication(self, user: dict, db: AsyncSession) -> bool:
        if user["authentication_method"] in EXTERNAL_AUTH_METHODS:
            return True

        if user["authentication_method"] == "default":
            tenant = await self._dao.tenant.get(user["tenant_uuid"], session=db)
            if tenant["default_authentication_method"] in EXTERNAL_AUTH_METHODS:
                return True
        return False

    async def assert_user_in_subtenant(
        self, scoping_tenant_uuid: str, user_uuid: str, db: AsyncSession
    ) -> None:
        """Asserts that a user belongs to a subtenant of the scoping tenant.

        Raises:
            UnknownUserException: If the user is not found or doesn't belong to
                a subtenant of the scoping tenant.
        """
        visible_tenants = await self._dao.tenant.list_visible_tenants(
            scoping_tenant_uuid, session=db
        )
        visible_tenants_uuids = [tenant.uuid for tenant in visible_tenants]
        if not await self._dao.user.exists(
            user_uuid, tenant_uuids=visible_tenants_uuids, session=db
        ):
            raise exceptions.UnknownUserException(user_uuid)

    async def _get_scoped_tenant_uuids(
        self, scoping_tenant_uuid: str, recurse: bool, db: AsyncSession
    ) -> list[str]:
        """Gets the UUIDs of all tenants visible from a scoping tenant.

        Args:
            scoping_tenant_uuid: The UUID of the scoping tenant.
            recurse: Whether to include subtenants recursively.

        Returns:
            A list of tenant UUIDs.
        """
        from accent_auth.services.tenant import (
            TenantService,
        )  # Avoid circular import

        if not recurse:
            return [scoping_tenant_uuid]
        tenant_service = TenantService(
            self._dao, None, None
        )  # all_users_policies and bus publisher are not used
        visible_tenants = await tenant_service.list_sub_tenants(
            scoping_tenant_uuid, db=db
        )

        return visible_tenants
