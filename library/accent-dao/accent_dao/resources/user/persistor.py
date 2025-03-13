# file: accent_dao/resources/user/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import String, and_, cast, func, literal_column, select

from accent_dao.alchemy.func_key_template import FuncKeyTemplate
from accent_dao.alchemy.userfeatures import UserFeatures as User
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.user.fixes import UserFixes
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.alchemy.groupfeatures import GroupFeatures as Group

logger = logging.getLogger(__name__)


class UserPersistor(CriteriaBuilderMixin, AsyncBasePersistor[User]):
    """Persistor class for User model."""

    _search_table = User

    def __init__(
        self,
        session: AsyncSession,
        view: Any,  # Corrected to Any
        search_system: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize UserPersistor.

        Args:
            session: Async database session.
            search_system: Search system for users.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.view = view
        self.search_system = search_system
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find users based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(User)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def find_by_id_uuid(self, id: int | str) -> User | None:
        """Find a user by id or uuid.

        Args:
            id (int | str): the id or the uuid

        Returns:
            User| None

        """
        if isinstance(id, int) or id.isdigit():
            query = select(User).filter(User.id == int(id))
        else:
            query = select(User).filter(User.uuid == id)
        if self.tenant_uuids is not None:
            query = query.filter(User.tenant_uuid.in_(self.tenant_uuids))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id_uuid(self, id: int | str) -> User:
        """Get by id or uuid.

        Args:
            id (int | str): The id or uuid

        Returns:
            User

        Raises:
            NotFoundError

        """
        user = await self.find_by_id_uuid(id)
        if not user:
            raise errors.NotFoundError("User", id=id)

        return user

    async def find_all_by_agent_id(self, agent_id: int) -> list[User]:
        """Find all users for given agent id.

        Args:
            agent_id (int)

        Returns:
            list[User]

        """
        result = await self.session.execute(
            select(User).filter(User.agentid == agent_id)
        )
        return list(result.scalars().all())

    async def count_all_by(self, column_name: str, criteria: dict) -> list:
        """Count all users grouped by a column.

        Args:
            column_name (str): Column name to group by.
            criteria (dict): filtering criteria

        Returns:
            list

        """
        column = self._get_column(column_name)
        query = select(column, func.count(column).label("count"))
        query = self.build_criteria(query, criteria)
        if self.tenant_uuids is not None:
            query = query.filter(User.tenant_uuid.in_(self.tenant_uuids))
        query = query.group_by(column)
        result = await self.session.execute(query)
        return result.all()

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for users.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = self.view.query(self.session)
        if self.tenant_uuids is not None:
            query = query.filter(User.tenant_uuid.in_(self.tenant_uuids))

        return await self.search_system.async_search_from_query(
            self.session, query, parameters
        )

    async def search_collated(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for users with collated results.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = self.view.query(self.session)
        if self.tenant_uuids is not None:
            query = query.filter(User.tenant_uuid.in_(self.tenant_uuids))
        return await self.search_system.async_search_from_query_collated(
            self.session, query, parameters
        )

    async def create(self, user: User) -> User:
        """Create a new user.

        Args:
            user: The user object to create.

        Returns:
            The created user object.

        """
        self._prepare_template(user)
        user.fill_caller_id()
        return await super().create(user)

    def _prepare_template(self, user: User) -> None:
        """Prepare the function key template for the user.

        Args:
            user: The user object.

        """
        if not user.func_key_private_template_id:
            template = FuncKeyTemplate(tenant_uuid=user.tenant_uuid, private=True)
            user.func_key_template_private = template

    async def edit(self, user: User) -> None:
        """Edit an existing user.

        Args:
            user: The user object to edit.

        """
        user.fill_caller_id()
        await super().edit(user)
        await UserFixes(self.session).async_fix(user.id)

    async def associate_all_groups(self, user: User, groups: list[Group]) -> None:
        """Associate all provided groups with the user.

        Args:
            user: The user object.
            groups: List of Group objects to associate.

        """
        with self.session.no_autoflush:
            user.groups = groups
            for member in user.group_members:
                member.user = user
                member.fix()
        await self.session.flush()

    async def list_outgoing_callerid_associated(self, user_id: int) -> list:
        """List the outgoing caller IDs associated with a user.

        Args:
            user_id: The ID of the user.

        Returns:
            List of associated outgoing caller IDs.

        """
        from accent_dao.alchemy.dialaction import Dialaction
        from accent_dao.alchemy.extension import Extension
        from accent_dao.alchemy.incall import Incall

        stmt = (
            select(
                Extension.exten.label("number"),
                literal_column("'associated'").label("type"),
            )
            .select_from(Incall)
            .join(
                Dialaction,
                and_(
                    Dialaction.category == "incall",
                    Dialaction.categoryval == cast(Incall.id, String),
                ),
            )
            .join(
                Extension,
                and_(
                    Extension.type == "incall",
                    Extension.typeval == cast(Incall.id, String),
                ),
            )
            .filter(
                and_(
                    Dialaction.action == "user",
                    Dialaction.actionarg1 == str(user_id),
                )
            )
        )

        result = await self.session.execute(stmt)
        return result.all()
