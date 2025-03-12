# file: accent_dao/models/contextinclude.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .context import Context


class ContextInclude(Base):
    """Represents an inclusion of one context within another.

    Attributes:
        context: The name of the context being included in.
        include: The name of the context to include.
        priority: The priority of the inclusion.
        included_context: Relationship to the included Context.
    """

    __tablename__: str = "contextinclude"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ("context",),
            ("context.name",),
            ondelete="CASCADE",
        ),
    )

    context: Mapped[str] = mapped_column(String(79), primary_key=True)
    include: Mapped[str] = mapped_column(String(79), primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    included_context: Mapped["Context"] = relationship(
        "Context",
        primaryjoin="Context.name == ContextInclude.include",
        foreign_keys="ContextInclude.include",
        uselist=False,
    )
