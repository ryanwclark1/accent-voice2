# file: accent_dao/resources/utils/view.py
# Copyright 2025 Accent Communications

import abc
from typing import TYPE_CHECKING, Any, TypeVar

from sqlalchemy import select

from accent_dao.helpers import errors

if TYPE_CHECKING:
    from sqlalchemy.orm.strategy_options import LoaderOption

    QueryOptions = tuple[LoaderOption, ...]
    SyncQuery = Any  # Replace with the actual type if you have a specific Query type
    AsyncQuery = (
        Any  # Replace with the actual type if you have a specific AsyncQuery type
    )

from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

_T = TypeVar("_T")


class ViewSelector:
    """A class for selecting different views of a resource.

    This class allows for defining and selecting different "views" of a resource,
    which can be used to control what data is returned and how it's formatted.

    Attributes:
        default: The default view to use if no view is specified.
        views: A dictionary mapping view names to view objects.

    """

    def __init__(self, default: "View", **views: "View") -> None:
        """Initialize a ViewSelector.

        Args:
            default: The default view object.
            **views: Keyword arguments representing view names and their
                corresponding view objects.

        """
        self.default = default
        self.views = views

    def select(self, name: str | None = None) -> "View":
        """Select a view by name.

        Args:
            name: The name of the view to select. If None, the default view is returned.

        Returns:
            The selected view object.

        Raises:
            InputError: If a view with the given name is not found.

        """
        if name is None:
            return self.default
        if name not in self.views:
            raise errors.InputError(f"Invalid view name: {name}")
        return self.views[name]


class View(metaclass=abc.ABCMeta):
    """Abstract base class for defining views of a resource.

    Subclasses should implement the `query` and `convert` methods
    to define how data is retrieved and transformed for a specific view.
    """

    @abc.abstractmethod
    async def query(self, session: Session | AsyncSession) -> Any:  # Changed to async
        """Define the query for the view.

        Args:
            session: The database session (can be sync or async).

        Returns:
            The query object.

        """
        ...

    @abc.abstractmethod
    def convert(self, row: Any) -> Any:  # Use Any for row
        """Convert a database row to the desired view format.

        Args:
            row: Row data from database.

        Returns:
            The converted output.

        """
        ...

    def convert_list(self, rows: Sequence[Any]) -> list[Any]:  # More specific type
        """Convert a list of rows to the desired view format.

        Args:
            rows: A list of database rows.

        Returns:
            A list of the converted output.

        """
        return [self.convert(row) for row in rows]


class ModelView(View):
    """A view that converts database rows to model instances.

    Attributes:
        table: The SQLAlchemy table to query.
        db_converter: A converter object for mapping db columns to model attributes.

    """

    @property
    @abc.abstractmethod
    def table(self) -> Any:  # Use Any; specific table type not known here
        """Return table property."""
        ...

    @property
    @abc.abstractmethod
    def db_converter(self) -> Any:  # Use Any; converter type not known here.
        """Return a database converter."""
        ...

    def query(self, session: Session | AsyncSession) -> Any:  # Use Any for query
        """Define the query for the view.

        Args:
            session: The database session.

        Returns:
            The SQLAlchemy query object.

        """
        # Adapt based on session type (sync or async)
        if isinstance(session, AsyncSession):
            return select(self.table)  # Use select for async
        else:
            return session.query(self.table)  # type: ignore

    def convert(self, row: Any) -> Any:  # Use Any for row
        """Convert a database row to a model instance.

        Args:
            row: The database row.

        Returns:
            The model instance.

        """
        return self.db_converter.to_model(row)
