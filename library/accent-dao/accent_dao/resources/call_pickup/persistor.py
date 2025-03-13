# /resources/call_pickup/persistor.py
# Copyright 2025 Accent Communications

import logging
from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from accent_dao.alchemy.pickup import Pickup as CallPickup
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

logger = logging.getLogger(__name__)


class CallPickupPersistor(CriteriaBuilderMixin, BasePersistor):
    """Persistor for CallPickup objects.

    Handles CRUD operations and search functionality for call pickup objects.
    """

    _search_table = CallPickup

    def __init__(
        self,
        session: Session | AsyncSession,
        call_pickup_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize the CallPickupPersistor.

        Args:
            session: SQLAlchemy session (sync or async)
            call_pickup_search: Search system for call pickups
            tenant_uuids: Optional list of tenant UUIDs

        """
        self.session = session
        self.search_system = call_pickup_search
        self.tenant_uuids = tenant_uuids
        self.is_async = isinstance(session, AsyncSession)

    def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build query for finding call pickups based on criteria.

        Args:
            criteria: Search criteria

        Returns:
            SQLAlchemy query object

        """
        query = self.session.query(CallPickup)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _async_find_query(self, criteria: dict[str, Any]) -> Any:
        """Build async query for finding call pickups based on criteria.

        Args:
            criteria: Search criteria

        Returns:
            SQLAlchemy async query object

        """
        query = select(CallPickup)
        query = self._async_filter_tenant_uuid(query)
        return self.async_build_criteria(query, criteria)

    def get_by(self, criteria: dict[str, Any]) -> Any:
        """Get a call pickup by criteria.

        Args:
            criteria: Search criteria

        Returns:
            Call pickup object

        Raises:
            NotFoundError: If call pickup is not found

        """
        model = self.find_by(criteria)
        if not model:
            logger.error("CallPickup not found with criteria: %s", criteria)
            raise errors.not_found("CallPickup", **criteria)
        return model

    async def async_get_by(self, criteria: dict[str, Any]) -> Any:
        """Get a call pickup by criteria asynchronously.

        Args:
            criteria: Search criteria

        Returns:
            Call pickup object

        Raises:
            NotFoundError: If call pickup is not found

        """
        model = await self.async_find_by(criteria)
        if not model:
            logger.error("CallPickup not found with criteria: %s", criteria)
            raise errors.not_found("CallPickup", **criteria)
        return model

    def _search_query(self) -> Any:
        """Build base search query.

        Returns:
            SQLAlchemy query object

        """
        return self.session.query(self.search_system.config.table)

    async def _async_search_query(self) -> Any:
        """Build base async search query.

        Returns:
            SQLAlchemy async query object

        """
        return select(self.search_system.config.table)

    def create(self, call_pickup: Any) -> Any:
        """Create a new call pickup.

        Args:
            call_pickup: Call pickup object to create

        Returns:
            Created call pickup object

        """
        self._fill_default_values(call_pickup)
        self.session.add(call_pickup)
        self.session.flush()
        logger.info("Created call pickup with ID %s", call_pickup.id)
        return call_pickup

    async def async_create(self, call_pickup: Any) -> Any:
        """Create a new call pickup asynchronously.

        Args:
            call_pickup: Call pickup object to create

        Returns:
            Created call pickup object

        """
        await self._async_fill_default_values(call_pickup)
        self.session.add(call_pickup)
        await self.session.flush()
        logger.info("Created call pickup with ID %s asynchronously", call_pickup.id)
        return call_pickup

    def _fill_default_values(self, call_pickup: Any) -> None:
        """Fill default values for a call pickup.

        Args:
            call_pickup: Call pickup object to update

        """
        last_id = (
            self.session.query(CallPickup.id)
            .order_by(CallPickup.id.desc())
            .limit(1)
            .scalar()
        )
        call_pickup.id = 1 if last_id is None else last_id + 1

    async def _async_fill_default_values(self, call_pickup: Any) -> None:
        """Fill default values for a call pickup asynchronously.

        Args:
            call_pickup: Call pickup object to update

        """
        stmt = select(CallPickup.id).order_by(desc(CallPickup.id)).limit(1)
        result = await self.session.execute(stmt)
        last_id = result.scalar()
        call_pickup.id = 1 if last_id is None else last_id + 1

    def associate_interceptor_users(self, call_pickup: Any, users: list[Any]) -> None:
        """Associate interceptor users with a call pickup.

        Args:
            call_pickup: Call pickup object
            users: List of user objects to associate

        """
        call_pickup.user_interceptors = users
        self.session.flush()
        logger.debug(
            "Associated %s interceptor users with call pickup ID %s",
            len(users),
            call_pickup.id,
        )

    async def async_associate_interceptor_users(
        self, call_pickup: Any, users: list[Any]
    ) -> None:
        """Associate interceptor users with a call pickup asynchronously.

        Args:
            call_pickup: Call pickup object
            users: List of user objects to associate

        """
        call_pickup.user_interceptors = users
        await self.session.flush()
        logger.debug(
            "Associated %s interceptor users with call pickup ID %s asynchronously",
            len(users),
            call_pickup.id,
        )

    def associate_target_users(self, call_pickup: Any, users: list[Any]) -> None:
        """Associate target users with a call pickup.

        Args:
            call_pickup: Call pickup object
            users: List of user objects to associate

        """
        call_pickup.user_targets = users
        self.session.flush()
        logger.debug(
            "Associated %s target users with call pickup ID %s",
            len(users),
            call_pickup.id,
        )

    async def async_associate_target_users(
        self, call_pickup: Any, users: list[Any]
    ) -> None:
        """Associate target users with a call pickup asynchronously.

        Args:
            call_pickup: Call pickup object
            users: List of user objects to associate

        """
        call_pickup.user_targets = users
        await self.session.flush()
        logger.debug(
            "Associated %s target users with call pickup ID %s asynchronously",
            len(users),
            call_pickup.id,
        )

    def associate_interceptor_groups(self, call_pickup: Any, groups: list[Any]) -> None:
        """Associate interceptor groups with a call pickup.

        Args:
            call_pickup: Call pickup object
            groups: List of group objects to associate

        """
        call_pickup.group_interceptors = groups
        self.session.flush()
        logger.debug(
            "Associated %s interceptor groups with call pickup ID %s",
            len(groups),
            call_pickup.id,
        )

    async def async_associate_interceptor_groups(
        self, call_pickup: Any, groups: list[Any]
    ) -> None:
        """Associate interceptor groups with a call pickup asynchronously.

        Args:
            call_pickup: Call pickup object
            groups: List of group objects to associate

        """
        call_pickup.group_interceptors = groups
        await self.session.flush()
        logger.debug(
            "Associated %s interceptor groups with call pickup ID %s asynchronously",
            len(groups),
            call_pickup.id,
        )

    def associate_target_groups(self, call_pickup: Any, groups: list[Any]) -> None:
        """Associate target groups with a call pickup.

        Args:
            call_pickup: Call pickup object
            groups: List of group objects to associate

        """
        call_pickup.group_targets = groups
        self.session.flush()
        logger.debug(
            "Associated %s target groups with call pickup ID %s",
            len(groups),
            call_pickup.id,
        )

    async def async_associate_target_groups(
        self, call_pickup: Any, groups: list[Any]
    ) -> None:
        """Associate target groups with a call pickup asynchronously.

        Args:
            call_pickup: Call pickup object
            groups: List of group objects to associate

        """
        call_pickup.group_targets = groups
        await self.session.flush()
        logger.debug(
            "Associated %s target groups with call pickup ID %s asynchronously",
            len(groups),
            call_pickup.id,
        )

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID.

        Args:
            query: SQLAlchemy query object

        Returns:
            Filtered query object

        """
        if self.tenant_uuids is None:
            return query
        return query.filter(CallPickup.tenant_uuid.in_(self.tenant_uuids))

    def _async_filter_tenant_uuid(self, query: Any) -> Any:
        """Filter async query by tenant UUID.

        Args:
            query: SQLAlchemy async query object

        Returns:
            Filtered query object

        """
        if self.tenant_uuids is None:
            return query
        return query.where(CallPickup.tenant_uuid.in_(self.tenant_uuids))

    async def async_find_by(self, criteria: dict[str, Any]) -> Any | None:
        """Find a call pickup by criteria asynchronously.

        Args:
            criteria: Search criteria

        Returns:
            Call pickup object or None if not found

        """
        query = await self._async_find_query(criteria)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def async_find_all_by(self, criteria: dict[str, Any]) -> list[Any]:
        """Find all call pickups matching criteria asynchronously.

        Args:
            criteria: Search criteria

        Returns:
            List of matching call pickup objects

        """
        query = await self._async_find_query(criteria)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def async_edit(self, call_pickup: Any) -> None:
        """Edit an existing call pickup asynchronously.

        Args:
            call_pickup: Call pickup object to edit

        """
        # In SQLAlchemy 2.0, the session will automatically track changes
        await self.session.flush()
        logger.info("Edited call pickup with ID %s asynchronously", call_pickup.id)

    async def async_delete(self, call_pickup: Any) -> None:
        """Delete a call pickup asynchronously.

        Args:
            call_pickup: Call pickup object to delete

        """
        await self.session.delete(call_pickup)
        await self.session.flush()
        logger.info("Deleted call pickup with ID %s asynchronously", call_pickup.id)

    async def async_search(self, parameters: dict[str, Any]) -> list[Any]:
        """Search for call pickups based on parameters asynchronously.

        Args:
            parameters: Search parameters

        Returns:
            List of matching call pickup objects

        """
        base_query = await self._async_search_query()
        query = await self.search_system.async_create_query(base_query, parameters)
        result = await self.session.execute(query)
        return result.scalars().all()
