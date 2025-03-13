# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.user_external_app import UserExternalApp
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class UserExternalAppPersistor(
    CriteriaBuilderMixin, AsyncBasePersistor[UserExternalApp]
):
    """Persistor class for UserExternalApp model."""

    _search_table = UserExternalApp

    def __init__(
        self, session: AsyncSession, user_external_app_search: Any, user_uuid: str
    ) -> None:
        """Initialize UserExternalAppPersistor.

        Args:
            session: Async database session.
            user_external_app_search: Search system for user external apps.
            user_uuid: The UUID of the user.

        """
        super().__init__(session, self._search_table)
        self.search_system = user_external_app_search
        self.user_uuid = user_uuid  # Store the user_uuid

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find user external apps based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(UserExternalApp).filter(
            UserExternalApp.user_uuid == self.user_uuid
        )  # Always filter by user_uuid
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching user external apps.

        Returns:
            SQLAlchemy query object.

        """
        return select(self.search_system.config.table).filter(
            UserExternalApp.user_uuid == self.user_uuid
        )  # Always filter by user_uuid

    async def get_by(self, criteria: dict[str, Any]) -> UserExternalApp:
        """Retrieve a single user external app by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            UserExternalApp: The found user external app.

        Raises:
            NotFoundError: If no user external app is found.

        """
        model = await self.find_by(criteria)
        if not model:
            criteria["user_uuid"] = self.user_uuid  # Include in error message
            raise errors.NotFoundError("UserExternalApp", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[UserExternalApp]:
        """Find all UserExternalApp by criteria.

        Returns:
            list of UserExternalApp.

        """
        result: Sequence[UserExternalApp] = await super().find_all_by(criteria)
        return list(result)
