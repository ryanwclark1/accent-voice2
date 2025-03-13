# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.groupfeatures import GroupFeatures as Group
from accent_dao.alchemy.rightcallmember import RightCallMember
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence
    from accent_dao.alchemy.queuemember import QueueMember
    from accent_dao.alchemy.rightcall import RightCall


class GroupPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Group]):
    """Persistor class for Group model."""

    _search_table = Group

    def __init__(
        self,
        session: AsyncSession,
        group_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize GroupPersistor.

        Args:
            session: Async database session.
            group_search: Search system for groups.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = group_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find groups based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Group)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching groups."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> Group:
        """Retrieve a single group by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Group: The found group.

        Raises:
            NotFoundError: If no group is found.

        """
        group = await self.find_by(criteria)
        if not group:
            logger.error("Group not found with criteria: %s", criteria)
            raise errors.NotFoundError("Group", **criteria)
        return group

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for groups.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = await self._search_query()
        query = self._filter_tenant_uuid(query)
        rows, total = await self.search_system.async_search_from_query(
            self.session, query, parameters
        )
        return SearchResult(total, rows)

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Group]:
        """Find all Group by criteria.

        Returns:
            list of Group.

        """
        result: Sequence[Group] = await super().find_all_by(criteria)
        return list(result)

    async def associate_all_member_users(
        self, group: Group, members: Sequence[QueueMember]
    ) -> None:
        """Associate all user members with a group.

        Args:
            group: Group to associate members with.
            members: Member list

        """
        group.user_queue_members = []
        for member in members:
            self._fill_user_queue_member_default_values(member)
            group.user_queue_members.append(member)
            member.fix()  # Assuming that member has a method called "fix()"
        await self.session.flush()

    def _fill_user_queue_member_default_values(self, member: "QueueMember") -> None:
        """Fill the default values for the membership.

        Args:
            member: queue member to set default

        """
        member.category = "group"
        member.usertype = "user"

    async def associate_all_member_extensions(
        self, group: Group, members: Sequence[QueueMember]
    ) -> None:
        """Associate all member extensions with a group.

        Args:
            group: Group to associate members with.
            members: Members list

        """
        group.extension_queue_members = []
        for member in members:
            self._fill_extension_queue_member_default_values(member)
            group.extension_queue_members.append(member)
            member.fix()  # Assuming that member has a method called "fix()"
        await self.session.flush()

    def _fill_extension_queue_member_default_values(
        self, member: "QueueMember"
    ) -> None:
        """Fill in the default values of extension members.

        Args:
            member: Member to set default

        """
        member.category = "group"
        member.usertype = "user"
        member.userid = 0

    async def associate_call_permission(
        self, group: Group, call_permission: "RightCall"
    ) -> None:
        """Associate a call permission with a group.

        Args:
            group: Group to associate
            call_permission: Call permission to associate

        """
        if call_permission not in group.call_permissions:
            group.call_permissions.append(call_permission)
            await self.session.flush()
            self.session.expunge(
                group, ["rightcall_members"]
            )  # Ensure 'rightcall_members' is expired

    async def dissociate_call_permission(
        self, group: Group, call_permission: "RightCall"
    ) -> None:
        """Dissociate a call permission from a group.

        Args:
            group: Group to dissociate
            call_permission: Call permission to dissociate

        """
        if call_permission in group.call_permissions:
            group.call_permissions.remove(call_permission)
            await self.session.flush()
            self.session.expunge(
                group, ["rightcall_members"]
            )  # Ensure 'rightcall_members' is expired
