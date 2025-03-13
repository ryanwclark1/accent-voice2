# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import String, and_, cast, delete, literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from accent_dao.alchemy.rightcallmember import RightCallMember
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.dialaction import Dialaction
    from accent_dao.alchemy.extension import Extension
    from accent_dao.alchemy.groupfeatures import GroupFeatures
    from accent_dao.alchemy.linefeatures import LineFeatures
    from accent_dao.alchemy.queuemember import QueueMember
    from accent_dao.alchemy.rightcall import RightCall
    from accent_dao.alchemy.schedule import Schedule
    from accent_dao.alchemy.schedulepath import SchedulePath


class UserPersistor(CriteriaBuilderMixin, AsyncBasePersistor[UserFeatures]):
    """Persistor class for UserFeatures model."""

    _search_table = UserFeatures

    def __init__(
        self,
        session: AsyncSession,
        user_view: Any,
        user_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize UserPersistor.

        Args:
            session: Async database session.
            user_view: View for user data.
            user_search: Search system for users.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.view = user_view
        self.search_system = user_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find users based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(UserFeatures)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> UserFeatures:
        """Retrieve a single user by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            UserFeatures: The found user.

        Raises:
            NotFoundError: If no user is found.

        """
        user = await self.find_by(criteria)
        if not user:
            raise errors.NotFoundError("User", **criteria)
        return user

    async def find_all_by(self, criteria: dict[str, Any]) -> list[UserFeatures]:
        """Find all UserFeatures by criteria.

        Returns:
            list of UserFeatures.

        """
        result: Sequence[UserFeatures] = await super().find_all_by(criteria)
        return list(result)

    async def get_by_id_uuid(self, id: int | str) -> UserFeatures:
        """Get a UserFeatures by ID or UUID.

        Args:
            id: ID or UUID of the user.

        Returns:
            UserFeatures object.

        Raises:
            NotFoundError: If no user with specified ID or UUID.

        """
        user = await self.find_by_id_uuid(id)
        if not user:
            raise errors.NotFoundError("User", id=id)
        return user

    async def find_by_id_uuid(self, id: int | str) -> UserFeatures | None:
        """Find a UserFeatures by ID or UUID.

        Args:
            id: ID or UUID of the user.

        Returns:
            UserFeatures object if found, otherwise None.

        """
        if isinstance(id, int) or id.isdigit():
            return await self.find_by({"id": int(id)})
        else:
            return await self.find_by({"uuid": id})

    async def create(self, user: UserFeatures) -> UserFeatures:
        """Create a UserFeatures.

        Args:
            user: UserFeatures object

        Returns:
            The created UserFeatures.

        """
        user.prepare_template()
        user.fill_caller_id()
        return await super().create(user)

    async def search(self, parameters: dict[str, Any]) -> Any:
        """Perform search using view with given parameters.

        Args:
            parameters: Search parameters.

        Returns:
            Search result.

        """
        view = self.view.select("default")
        query = view.query(self.session)
        if self.tenant_uuids is not None:
            query = query.filter(UserFeatures.tenant_uuid.in_(self.tenant_uuids))
        return await self.search_system.search_from_query(query, parameters)

    async def search_collated(self, parameters: dict[str, Any]) -> Any:
        """Perform collated search using view with given parameters.

        Args:
            parameters: Search parameters.

        Returns:
            Search result.

        """
        view = self.view.select("default")
        query = view.query(self.session)
        if self.tenant_uuids is not None:
            query = query.filter(UserFeatures.tenant_uuid.in_(self.tenant_uuids))
        return await self.search_system.search_from_query_collated(query, parameters)

    async def associate_all_groups(
        self, user: UserFeatures, groups: list["GroupFeatures"]
    ) -> None:
        """Associate all provided groups with a user.

        Args:
            user: The UserFeatures object.
            groups: List of GroupFeatures objects to associate.

        """
        user.groups = groups
        await self.session.flush()

    async def dissociate_call_permission(
        self, user: UserFeatures, call_permission: "RightCall"
    ) -> None:
        """Dissociate a call permission from a user.

        Args:
            user: The UserFeatures object.
            call_permission: The RightCall object to dissociate.

        """
        await self.session.execute(
            delete(RightCallMember)
            .where(RightCallMember.type == "user")
            .where(RightCallMember.typeval == str(user.id))
            .where(RightCallMember.rightcallid == call_permission.id)
        )
        await self.session.flush()

    async def list_outgoing_callerid_associated(
        self, user_id: int
    ) -> list[dict[str, str]]:
        """List outgoing caller ID associations for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of dictionaries, each with "number" and "type" keys.

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
        return [{"number": row.number, "type": row.type} for row in result.all()]
