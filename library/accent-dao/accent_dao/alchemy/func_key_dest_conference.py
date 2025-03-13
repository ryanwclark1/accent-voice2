# file: accent_dao/alchemy/func_key_dest_conference.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .conference import Conference
    from .func_key import FuncKey


class FuncKeyDestConference(Base):
    """Represents a function key destination for a conference room.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 4).
        conference_id: The ID of the associated conference room.
        type: The type of destination ('conference').
        func_key: Relationship to FuncKey.
        conference: Relationship to Conference.

    """

    DESTINATION_TYPE_ID: int = 4

    __tablename__: str = "func_key_dest_conference"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )
    conference_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conference.id", ondelete="CASCADE"), primary_key=True
    )

    type: str = "conference"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    conference: Mapped["Conference"] = relationship("Conference")

    def to_tuple(self) -> tuple[tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (("conference_id", self.conference_id),)
