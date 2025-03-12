# file: accent_dao/resources/utils/search.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, NamedTuple, TypeVar

import sqlalchemy as sa
from sqlalchemy import func, or_, text
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from sqlalchemy.types import Integer, String
from unidecode import unidecode

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session

from accent_dao.helpers import errors  # Import errors module

logger: logging.Logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class SearchResult(NamedTuple):
    """Represents the result of a search operation.

    Attributes:
        total: The total number of records matching the search criteria.
        items: The list of records returned for the current page.

    """

    total: int
    items: list[Any]


class unaccent(ReturnTypeFromArgs):  # type: ignore
    """Custom SQL function for unaccenting strings."""

    cache_ok = True


class SearchConfig:
    """Configuration class for defining search behavior.

    Attributes:
        table: The SQLAlchemy table to search against.
        columns: A dictionary mapping search field names to SQLAlchemy column objects.
        default_sort: The default column to sort by if no sort order is specified.
        search: An optional list of column names to be used for full-text search.
                If None, all columns in 'columns' will be used for searching.
        sort: An optional list of valid column names that can be used for sorting.
              If None, all columns in 'columns' can be used for sorting.

    """

    def __init__(
        self,
        table: Any,
        columns: dict[str, Any],
        default_sort: str,
        search: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> None:
        """Initialize SearchConfig.

        Args:
            table: The SQLAlchemy table to search against.
            columns: A dictionary mapping search field names to
                SQLAlchemy column objects.
            default_sort: The default column to sort by if no sort order is specified.
            search: An optional list of column names to
                be used for full-text search. Defaults to None.
            sort: An optional list of valid column names
                that can be used for sorting. Defaults to None.

        Raises:
            ValueError: If the `default_sort` is not a valid column name,
                        or `sort` contains invalid column names.

        """
        self.table = table
        self._columns = columns
        if default_sort not in self._columns:
            raise ValueError(
                f"Default sort column '{default_sort}' not in available columns: {list(columns.keys())}"
            )
        self._default_sort = default_sort

        if search is None:
            self._search = list(self._columns.keys())
        else:
            for col in search:
                if col not in self._columns:
                    raise ValueError(f"Search column '{col}' not in available columns")
            self._search = search

        if sort is not None:
            for col in sort:
                if col not in self._columns:
                    raise ValueError(f"Sort column '{col}' not in available columns")
            self._sort = sort
        else:
            self._sort = list(self._columns.keys())

    def all_search_columns(self) -> list:
        """Return all columns that can be used for searching."""
        return [self._columns[s] for s in self._search]

    def column_for_searching(self, column_name: str) -> Any | None:
        """Return the SQLAlchemy column object for a given column name."""
        return self._columns.get(column_name)

    def column_for_sorting(self, name: str | None = None) -> Any:
        """Return the SQLAlchemy column object for sorting.

        Args:
            name: The name of the column to sort by.

        Returns:
            The SQLAlchemy column object.

        Raises:
            ValueError: If an invalid sort column is provided.

        """
        column_name = self._get_sort_column_name(name)
        return self._columns[column_name]

    def _get_sort_column_name(self, name: str | None = None) -> str:
        """Get the column name for sorting, handling default and validation."""
        name = name or self._default_sort

        if name not in self._sort:
            raise ValueError(f"Invalid sort column '{name}'")

        return name


class CriteriaBuilderMixin:
    """Mixin class for building SQLAlchemy queries with criteria."""

    def build_criteria(
        self, query: Any, criteria: dict[str, Any]
    ) -> Any:  # Use Any for now
        """Build criteria for the query.

        Args:
            query: The SQLAlchemy query object.
            criteria: A dictionary of criteria to apply.

        Returns:
            The modified query with criteria applied.

        """
        for name, value in criteria.items():
            column = self._get_column(name)
            query = query.filter(column == value)
        return query

    @property
    def _search_table(self):
        raise NotImplementedError("Subclasses must implement _search_table")

    def _get_column(self, name: str) -> Any:
        """Get the SQLAlchemy column object by name.

        Args:
            name: The name of the column.

        Returns:
            The SQLAlchemy column object.

        Raises:
            KeyError: If the column name is not found.

        """
        column = getattr(self._search_table, name, None)
        if column is None:
            raise KeyError(f"Column {name} not found in search table")
        return column


class SearchSystem:
    """System for performing search queries with pagination and sorting.

    Attributes:
        config: SearchConfig object defining the search configuration.
        SORT_DIRECTIONS: Mapping of string direction names to SQLAlchemy functions.
        DEFAULTS: Default values for search parameters.

    """

    SORT_DIRECTIONS = {
        "asc": sa.asc,
        "desc": sa.desc,
    }

    DEFAULTS: dict[str, None | str | int] = {
        "search": None,
        "order": None,
        "direction": "asc",
        "limit": None,
        "offset": 0,
    }

    def __init__(self, config: SearchConfig) -> None:
        """Initialize the SearchSystem.

        Args:
            config: SearchConfig object.

        """
        self.config = config

    def search(
        self,
        session: Session,
        parameters: dict[str, Any] | None = None,
    ) -> SearchResult:
        """Perform a search using the provided parameters.

        Args:
            session: SQLAlchemy Session object.
            parameters: Dictionary of search parameters.

        Returns:
            SearchResult: NamedTuple containing total count and items.

        """
        query = session.query(self.config.table)
        return self.search_from_query(query, parameters)

    async def async_search(
        self,
        session: AsyncSession,
        parameters: dict[str, Any] | None = None,
    ) -> SearchResult:
        """Perform a search using the provided parameters.

        Args:
            session: SQLAlchemy AsyncSession object.
            parameters: Dictionary of search parameters.

        Returns:
            SearchResult: NamedTuple containing total count and items.

        """
        query = session.query(self.config.table)
        return await self.async_search_from_query(query, parameters)

    def search_from_query(
        self, query: Any, parameters: dict[str, Any] | None = None
    ) -> SearchResult:
        """Perform a search starting from an existing query.

        Args:
            query: SQLAlchemy query object.
            parameters: Dictionary of search parameters.

        Returns:
            SearchResult: NamedTuple containing total count and items.

        """
        parameters = self._populate_parameters(parameters)
        self._validate_parameters(parameters)

        query = self._filter(query, parameters["search"])
        query = self._filter_exact_match(query, parameters)
        sorted_query = self._sort(query, parameters["order"], parameters["direction"])
        paginated_query = self._paginate(
            sorted_query, parameters["limit"], parameters["offset"]
        )

        return SearchResult(sorted_query.count(), paginated_query.all())

    async def async_search_from_query(
        self,
        session: AsyncSession,
        query: Any,
        parameters: dict[str, Any] | None = None,
    ) -> SearchResult:
        """Async Perform a search starting from an existing query.

        Args:
            query: SQLAlchemy query object.
            parameters: Dictionary of search parameters.

        Returns:
            SearchResult: NamedTuple containing total count and items.

        """
        parameters = self._populate_parameters(parameters)
        self._validate_parameters(parameters)

        query = self._filter(query, parameters["search"])
        query = self._filter_exact_match(query, parameters)

        # Apply sorting
        sort_column_name = parameters["order"]
        sort_direction = parameters["direction"]
        query = self._sort(query, sort_column_name, sort_direction)

        # Apply pagination
        limit = parameters["limit"]
        offset = parameters["offset"]
        query = self._paginate(query, limit, offset)

        # Execute count and fetch queries concurrently using asyncio.gather
        count_query = sa.select(func.count()).select_from(query.subquery())
        count_task = session.execute(count_query)

        # Fetch the rows with the limit and offset using await
        result = await session.execute(query)
        rows = result.scalars().all()

        total = (await count_task).scalar_one()

        return SearchResult(total, rows)

    def _populate_parameters(
        self, parameters: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Populate parameters with default values if not provided.

        Args:
            parameters: Dictionary of search parameters.

        Returns:
            Dictionary with all parameters, including defaults.

        """
        new_params = dict(self.DEFAULTS)
        if parameters:
            new_params.update(parameters)
        return new_params

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Validate the provided search parameters.

        Args:
            parameters: Dictionary of search parameters.

        Raises:
            InputError: If any parameter is invalid.

        """
        if parameters["offset"] < 0:  # type: ignore
            raise errors.wrong_type("offset", "positive number")

        if parameters["limit"] is not None and parameters["limit"] <= 0:
            raise errors.wrong_type("limit", "positive number")

        if parameters["direction"] not in self.SORT_DIRECTIONS:
            raise errors.invalid_direction(parameters["direction"])

    def _filter(self, query: Any, term: str | None = None) -> Any:
        """Apply full-text search filtering to the query.

        Args:
            query: SQLAlchemy query object.
            term: Search term.

        Returns:
            The filtered query.

        """
        if not term:
            return query

        criteria = []
        for column in self.config.all_search_columns():
            clean_term = unidecode(term)
            expression = unaccent(sql.cast(column, String)).ilike(f"%{clean_term}%")
            criteria.append(expression)

        query = query.filter(sql.or_(*criteria))
        return query

    def _filter_exact_match(self, query: Any, parameters: dict[str, Any]) -> Any:
        """Apply exact match filtering for provided criteria.

        Args:
            query: SQLAlchemy query object.
            parameters: Dictionary of search parameters.

        Returns:
            The filtered query.

        """
        for column_name, value in parameters.items():
            column = self.config.column_for_searching(column_name)
            if column is not None:
                if isinstance(column.type, Integer) and not self._represents_int(value):
                    return query.filter(text("false"))
                query = query.filter(column == value)

        return query

    def _represents_int(self, value: Any) -> bool:
        """Check if a value can be converted to int."""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    def _sort(
        self, query: Any, order: str | None = None, direction: str = "asc"
    ) -> Any:
        """Apply sorting to the query.

        Args:
            query: SQLAlchemy query object.
            order: Column name to sort by.
            direction: Sort direction ('asc' or 'desc').

        Returns:
            The sorted query.

        """
        column = self.config.column_for_sorting(order)
        direction_func = self.SORT_DIRECTIONS[direction]

        return query.order_by(direction_func(column))

    def _paginate(self, query: Any, limit: int | None = None, offset: int = 0) -> Any:
        """Apply pagination to the query.

        Args:
            query: SQLAlchemy query object.
            limit: Maximum number of results per page.
            offset: Offset for pagination.

        Returns:
            The paginated query.

        """
        if offset > 0:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        return query
