# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.pickup import Pickup as CallPickup
from accent_dao.alchemy.pickupmember import PickupMember
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.groupfeatures import GroupFeatures
    from accent_dao.alchemy.userfeatures import UserFeatures


class CallPickupPersistor(CriteriaBuilderMixin, AsyncBasePersistor[CallPickup]):
    """Persistor class for CallPickup model."""

    _search_table = CallPickup

    def __init__(
        self,
        session: AsyncSession,
        call_pickup_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize CallPickupPersistor.

        Args:
            session: Async database session.
            call_pickup_search: Search system for call pickups.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = call_pickup_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find call pickups based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(CallPickup)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching call pickups."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> CallPickup:
        """Retrieve a single call pickup by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            CallPickup: The found call pickup.

        Raises:
            NotFoundError: If no call pickup is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("CallPickup", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[CallPickup]:
        """Find all CallPickup by criteria.

        Returns:
            list of CallPickup.

        """
        result: Sequence[CallPickup] = await super().find_all_by(criteria)
        return list(result)

    async def associate_interceptor_users(
        self, call_pickup: CallPickup, users: list["UserFeatures"]
    ) -> None:
        """Associate interceptor users with a call pickup.

        Args:
            call_pickup: Call pickup object.
            users: List of user objects to associate.

        """
        new_members = []
        for user in users:
            new_member = PickupMember(
                pickupid=call_pickup.id,
                category="member",
                membertype="user",
                memberid=user.id,
            )
            new_members.append(new_member)

        call_pickup.pickupmember_user_interceptors = new_members
        await self.session.flush()

    async def associate_target_users(
        self, call_pickup: CallPickup, users: list["UserFeatures"]
    ) -> None:
        """Associate target users with a call pickup.

        Args:
            call_pickup: Call pickup object.
            users: List of user objects to associate.

        """
        new_members = []
        for user in users:
            new_member = PickupMember(
                pickupid=call_pickup.id,
                category="pickup",
                membertype="user",
                memberid=user.id,
            )
            new_members.append(new_member)

        call_pickup.pickupmember_user_targets = new_members
        await self.session.flush()

    async def associate_interceptor_groups(
        self, call_pickup: CallPickup, groups: list["GroupFeatures"]
    ) -> None:
        """Associate interceptor groups with a call pickup.

        Args:
            call_pickup: Call pickup object.
            groups: List of group objects to associate.

        """
        new_members = []
        for group in groups:
            new_member = PickupMember(
                pickupid=call_pickup.id,
                category="member",
                membertype="group",
                memberid=group.id,
            )
            new_members.append(new_member)

        call_pickup.pickupmember_group_interceptors = new_members
        await self.session.flush()

    async def associate_target_groups(
        self, call_pickup: CallPickup, groups: list["GroupFeatures"]
    ) -> None:
        """Associate target groups with a call pickup.

        Args:
            call_pickup: Call pickup object.
            groups: List of group objects to associate.

        """
        new_members = []
        for group in groups:
            new_member = PickupMember(
                pickupid=call_pickup.id,
                category="pickup",
                membertype="group",
                memberid=group.id,
            )
            new_members.append(new_member)

        call_pickup.pickupmember_group_targets = new_members
        await self.session.flush()
