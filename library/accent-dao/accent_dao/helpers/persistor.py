# helpers/persistor.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Protocol,
    TypeVar,
)

from sqlalchemy import text

from accent_dao.helpers import errors
from accent_dao.resources.utils.search import SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Query, Session
    from sqlalchemy.sql import Select


class HasTenantUUID(Protocol):
    """Protocol for models with tenant_uuid attribute."""

    tenant_uuid: Any


T = TypeVar("T")
ModelType = TypeVar("ModelType", bound=HasTenantUUID)


class SearchSystem(Protocol):
    """Protocol for search system."""

    def search_from_query(
        self, query: Query, parameters: dict[str, Any]
    ) -> tuple[list[Any], int]:
        """Search using a query."""
        ...

    async def async_search_from_query(
        self, session: AsyncSession, stmt: Select, parameters: dict[str, Any]
    ) -> tuple[list[Any], int]:
        """Search asynchronously using a statement."""
        ...


class BasePersistor(Generic[ModelType]):
    """Base persistor class for database operations."""

    def __init__(
        self,
        session: Session,
        search_table: type[ModelType],
        tenant_uuids: list[str] | None = None,
        search_system: SearchSystem | None = None,
    ) -> None:
        """Initialize base persistor.

        Args:
            session: Database session
            search_table: Model class to search
            tenant_uuids: Optional list of tenant UUIDs to filter by
            search_system: Search system to use for search operations

        """
        self.session = session
        self._search_table = search_table
        self.tenant_uuids = tenant_uuids
        self.search_system = search_system

    def create(self, model: ModelType) -> ModelType:
        """Create a new record.

        Args:
            model: Model to create

        Returns:
            Created model

        """
        self.session.add(model)
        self.session.flush()
        return model

    def delete(self, model: ModelType) -> None:
        """Delete a record.

        Args:
            model: Model to delete

        """
        self.session.delete(model)
        self.session.flush()

    def edit(self, model: ModelType) -> None:
        """Edit a record.

        Args:
            model: Model to edit

        """
        self.persist(model)

    def find_by(self, criteria: dict[str, Any]) -> ModelType | None:
        """Find a record by criteria.

        Args:
            criteria: Criteria to filter by

        Returns:
            Found model or None

        """
        query = self._find_query(criteria)
        return query.first()

    def find_all_by(self, criteria: dict[str, Any]) -> Sequence[ModelType]:
        """Find all records by criteria.

        Args:
            criteria: Criteria to filter by

        Returns:
            List of found models

        """
        query = self._find_query(criteria)
        return query.all()

    def get_by(self, criteria: dict[str, Any]) -> ModelType:
        """Get a record by criteria.

        Args:
            criteria: Criteria to filter by

        Returns:
            Found model

        Raises:
            NotFoundError: If no record found

        """
        model = self.find_by(criteria)
        if not model:
            # Get class name for error message
            resource_name = self._search_table.__name__
            raise errors.not_found(resource_name, **criteria)
        return model

    def persist(self, model: ModelType) -> None:
        """Persist a model.

        Args:
            model: Model to persist

        """
        self.session.add(model)
        self.session.flush()
        self.session.expire(model)

    def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for records.

        Args:
            parameters: Search parameters

        Returns:
            Search result

        """
        if self.search_system is None:
            raise ValueError("Search system is required for search operations")

        query = self._search_query()
        query = self._filter_tenant_uuid(query)
        rows, total = self.search_system.search_from_query(query, parameters)
        return SearchResult(total, rows)

    def _find_query(self, criteria: dict[str, Any]) -> Query:
        """Create a query for finding records.

        Args:
            criteria: Criteria to filter by

        Returns:
            Query

        Raises:
            NotImplementedError: Method must be implemented by subclass

        """
        raise NotImplementedError

    def _search_query(self) -> Query:
        """Create a query for searching records.

        Returns:
            Query

        Raises:
            NotImplementedError: Method must be implemented by subclass

        """
        raise NotImplementedError

    def _filter_tenant_uuid(self, query: Query) -> Query:
        """Filter query by tenant UUID.

        Args:
            query: Query to filter

        Returns:
            Filtered query

        """
        if self.tenant_uuids is None:
            return query

        if not self.tenant_uuids:
            return query.filter(text("false"))

        # Access tenant_uuid through class attribute on the model class
        model_class = self._search_table
        return query.filter(model_class.tenant_uuid.in_(self.tenant_uuids))


class AsyncBasePersistor(Generic[ModelType]):
    """Base persistor class for async database operations."""

    def __init__(
        self,
        session: AsyncSession,
        search_table: type[ModelType],
        tenant_uuids: list[str] | None = None,
        search_system: SearchSystem | None = None,
    ) -> None:
        """Initialize async base persistor.

        Args:
            session: Async database session
            search_table: Model class to search
            tenant_uuids: Optional list of tenant UUIDs to filter by
            search_system: Search system to use for search operations

        """
        self.session = session
        self._search_table = search_table
        self.tenant_uuids = tenant_uuids
        self.search_system = search_system

    async def create(self, model: ModelType) -> ModelType:
        """Create a new record.

        Args:
            model: Model to create

        Returns:
            Created model

        """
        self.session.add(model)
        await self.session.flush()
        return model

    async def delete(self, model: ModelType) -> None:
        """Delete a record.

        Args:
            model: Model to delete

        """
        await self.session.delete(model)
        await self.session.flush()

    async def edit(self, model: ModelType) -> None:
        """Edit a record.

        Args:
            model: Model to edit

        """
        await self.persist(model)

    async def find_by(self, criteria: dict[str, Any]) -> ModelType | None:
        """Find a record by criteria.

        Args:
            criteria: Criteria to filter by

        Returns:
            Found model or None

        """
        stmt = await self._find_stmt(criteria)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_all_by(self, criteria: dict[str, Any]) -> Sequence[ModelType]:
        """Find all records by criteria.

        Args:
            criteria: Criteria to filter by

        Returns:
            List of found models

        """
        stmt = await self._find_stmt(criteria)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by(self, criteria: dict[str, Any]) -> ModelType:
        """Get a record by criteria.

        Args:
            criteria: Criteria to filter by

        Returns:
            Found model

        Raises:
            NotFoundError: If no record found

        """
        model = await self.find_by(criteria)
        if not model:
            resource_name = self._search_table.__name__
            raise errors.not_found(resource_name, **criteria)
        return model

    async def persist(self, model: ModelType) -> None:
        """Persist a model.

        Args:
            model: Model to persist

        """
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for records.

        Args:
            parameters: Search parameters

        Returns:
            Search result

        """
        if self.search_system is None:
            raise ValueError("Search system is required for search operations")

        stmt = await self._search_stmt()
        stmt = await self._filter_tenant_uuid(stmt)
        rows, total = await self.search_system.async_search_from_query(
            self.session, stmt, parameters
        )
        return SearchResult(total, rows)

    async def _find_stmt(self, criteria: dict[str, Any]) -> Select:
        """Create a statement for finding records.

        Args:
            criteria: Criteria to filter by

        Returns:
            Statement

        Raises:
            NotImplementedError: Method must be implemented by subclass

        """
        raise NotImplementedError

    async def _search_stmt(self) -> Select:
        """Create a statement for searching records.

        Returns:
            Statement

        Raises:
            NotImplementedError: Method must be implemented by subclass

        """
        raise NotImplementedError

    async def _filter_tenant_uuid(self, stmt: Select) -> Select:
        """Filter statement by tenant UUID.

        Args:
            stmt: Statement to filter

        Returns:
            Filtered statement

        """
        if self.tenant_uuids is None:
            return stmt

        if not self.tenant_uuids:
            return stmt.filter(text("false"))

        # Access tenant_uuid through class attribute on the model class
        model_class = self._search_table
        return stmt.filter(model_class.tenant_uuid.in_(self.tenant_uuids))
