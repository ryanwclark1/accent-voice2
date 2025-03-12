# file: accent_dao/models/asterisk_file_section.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .asterisk_file_variable import AsteriskFileVariable


class AsteriskFileSection(Base):
    """Represents a section within an Asterisk configuration file.

    Attributes:
        id: The unique identifier for the section.
        name: The name of the section.
        priority: The priority of the section.
        asterisk_file_id: The ID of the associated Asterisk file.
        variables: Relationship to AsteriskFileVariable, ordered by priority.

    """

    __tablename__: str = "asterisk_file_section"
    __table_args__: tuple = (
        UniqueConstraint("name", "asterisk_file_id"),
        Index("asterisk_file_section__idx__asterisk_file_id", "asterisk_file_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True)
    asterisk_file_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("asterisk_file.id", ondelete="CASCADE"),
        nullable=False,
    )

    variables: Mapped[list["AsteriskFileVariable"]] = relationship(
        "AsteriskFileVariable",
        order_by="AsteriskFileVariable.priority",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
