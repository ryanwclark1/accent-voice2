# file: accent_dao/resources/user_call_permission/persistor.py
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import cast as sql_cast
from sqlalchemy.types import Integer

from accent_dao.alchemy.rightcallmember import RightCallMember as UserCallPermission
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor

if TYPE_CHECKING:
    from collections.abc import Sequence
    from accent_dao.alchemy.userfeatures import UserFeatures
    from accent_dao.alchemy.rightcall import RightCall

logger = logging.getLogger(__name__)


class UserCallPermissionPersistor(AsyncBasePersistor[UserCallPermission]):
    """Persistor class for UserCallPermission model."""

    _search_table = UserCallPermission

    def __init__(self, session: AsyncSession) -> None:
        """Initialize UserCallPermissionPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find user call permissions based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(UserCallPermission).filter(
            UserCallPermission.type == "user"
        )  # Fixed: Corrected this.
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> UserCallPermission:
        """Retrieve a single user call permission by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            UserCallPermission: The found user call permission.

        Raises:
            NotFoundError: If no user call permission is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("UserCallPermission", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[UserCallPermission]:
        """Find all UserCallPermission by criteria.

        Returns:
            list of UserCallPermission.

        """
        result: Sequence[UserCallPermission] = await super().find_all_by(criteria)
        return list(result)

    async def associate_user_call_permission(
        self, user: UserFeatures, call_permission: RightCall
    ) -> UserCallPermission:
        """Associate a user with a call permission.

        If a UserCallPermission already exists for the given user and call permission,
        it is returned. Otherwise, a new UserCallPermission is created.

        Args:
            user: The UserFeatures object.
            call_permission: The RightCall object.

        Returns:
            The existing or newly created UserCallPermission object.

        """
        user_call_permission = await self.find_by(
            user_id=user.id, call_permission_id=call_permission.id
        )
        if not user_call_permission:
            user_call_permission = UserCallPermission(
                user_id=user.id,
                rightcallid=call_permission.id,
                type="user",
                typeval=str(user.id),
            )
            self.session.add(user_call_permission)
            await self.session.flush()
        return user_call_permission

    async def dissociate_user_call_permission(
        self, user: UserFeatures, call_permission: RightCall
    ) -> None:
        """Dissociate a user from a call permission.

        If a UserCallPermission exists for the given user and call permission,
        it is deleted.

        Args:
            user: The UserFeatures object.
            call_permission: The RightCall object.

        """
        user_call_permission = await self.find_by(
            user_id=user.id, call_permission_id=call_permission.id
        )
        if user_call_permission:
            await self.session.delete(user_call_permission)
            await self.session.flush()

    async def dissociate_all_call_permissions_by_user(self, user: UserFeatures) -> None:
        """Dissociate all call permissions from a user.

        Args:
            user: The UserFeatures object.

        """
        user_call_permissions = await self.find_all_by(user_id=user.id)
        for user_call_permission in user_call_permissions:
            await self.session.delete(user_call_permission)
        await self.session.flush()
