# helpers/db_views.py
# Copyright 2025 Accent Communications
from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from sqlalchemy import Table, text
from sqlalchemy.event import contains, listens_for, remove
from sqlalchemy.exc import InvalidRequestError

from accent_dao.helpers.db_manager import Base, SyncSession, get_async_session

if TYPE_CHECKING:
    from collections.abc import Callable

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session
    from sqlalchemy.orm.unitofwork import UOWTransaction


class MaterializedView(Base):
    """Materialized View base class.

    Used to tell SQLAlchemy to construct a materialized view.

    Usage:
        Assign the '__table__' attribute using the create_materialized_view function.

    Attributes:
        __abstract__: Flag to mark this class as abstract.
        __view_dependencies__: Tuple of model classes this view depends on.
        _view_dependencies_handler: Event handler for auto-refresh functionality.

    """

    __abstract__ = True
    __view_dependencies__: ClassVar[tuple[type[Base], ...]] = tuple()
    _view_dependencies_handler: ClassVar[
        Callable[[Session, UOWTransaction], None] | None
    ] = None
    _async_dependencies_handler: ClassVar[
        Callable[[AsyncSession, Any], None] | None
    ] = None

    def __init_subclass__(cls) -> None:
        """Initialize the subclass with materialized view functionality.

        Raises:
            InvalidRequestError: If __table__ attribute isn't created properly.

        """
        if not isinstance(getattr(cls, "__table__", None), Table):
            raise InvalidRequestError(
                f"Class '{cls}' '__table__' attribute must be created with 'create_materialized_view'"
            )
        super().__init_subclass__()

        if targets := cls.__view_dependencies__:
            # Sync handler
            @listens_for(SyncSession, "after_flush")
            def _after_flush_handler(
                session: Session, flush_context: UOWTransaction
            ) -> None:
                for obj in session.dirty | session.new | session.deleted:
                    if isinstance(obj, targets):
                        # Cannot call `refresh_materialized_view` as it will try to flush again.
                        session.execute(
                            text(
                                f"REFRESH MATERIALIZED VIEW CONCURRENTLY {cls.__table__.fullname}"
                            )
                        )
                        return

            cls._view_dependencies_handler = _after_flush_handler

            # Async handler implementation (reserved for future feature)
            # Note: SQLAlchemy event system doesn't have direct async support yet
            # This is a placeholder for future implementation
            cls._async_dependencies_handler = None
        else:
            cls._view_dependencies_handler = None
            cls._async_dependencies_handler = None

    @classmethod
    @property
    def autorefresh(cls) -> bool:
        """Check if autorefresh is enabled for this view.

        Returns:
            bool: True if autorefresh is enabled.

        """
        if handler := cls._view_dependencies_handler:
            return contains(SyncSession, "after_flush", handler)
        return False

    @classmethod
    def enable_autorefresh(cls) -> None:
        """Enable auto-refreshing of the materialized view."""
        if handler := cls._view_dependencies_handler:
            if not contains(SyncSession, "after_flush", handler):
                listens_for(SyncSession, "after_flush")(handler)

    @classmethod
    def disable_autorefresh(cls) -> None:
        """Disable auto-refreshing of the materialized view."""
        if handler := cls._view_dependencies_handler:
            if contains(SyncSession, "after_flush", handler):
                remove(SyncSession, "after_flush", handler)

    @classmethod
    def refresh(cls, concurrently: bool = True) -> None:
        """Refresh the materialized view synchronously.

        Args:
            concurrently: Whether to refresh concurrently (non-blocking).

        """
        with SyncSession() as session:
            refresh_stmt = text(
                f"REFRESH MATERIALIZED VIEW {'CONCURRENTLY ' if concurrently else ''}"
                f"{cls.__table__.fullname}"
            )
            session.execute(refresh_stmt)
            session.commit()

    @classmethod
    async def async_refresh(cls, concurrently: bool = True) -> None:
        """Refresh the materialized view asynchronously.

        Args:
            concurrently: Whether to refresh concurrently (non-blocking).

        """
        async with get_async_session() as session:
            refresh_stmt = text(
                f"REFRESH MATERIALIZED VIEW {'CONCURRENTLY ' if concurrently else ''}"
                f"{cls.__table__.fullname}"
            )
            await session.execute(refresh_stmt)
            await session.commit()


def create_materialized_view(
    name: str, selectable: Any, schema: str | None = None
) -> Table:
    """Create a materialized view table definition.

    Args:
        name: Name of the view.
        selectable: SQLAlchemy selectable object defining the view.
        schema: Optional schema name.

    Returns:
        Table: SQLAlchemy table object for the materialized view.

    """
    return Table(
        name,
        Base.metadata,
        info=dict(is_materialized_view=True, selectable=selectable),
        schema=schema,
    )
