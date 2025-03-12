# file: accent_dao/models/func_key_dest_bsfilter.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .callfiltermember import Callfiltermember
    from .func_key import FuncKey


class FuncKeyDestBSFilter(Base):
    """Represents a function key destination for a boss-secretary filter member.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 12).
        filtermember_id: The ID of the associated call filter member.
        type: The type of the destination ('bsfilter').
        func_key: Relationship to FuncKey.
        filtermember: Relationship to Callfiltermember.
        filter_member_id: The ID of the filter member (same as filtermember_id).

    """

    DESTINATION_TYPE_ID: int = 12

    __tablename__: str = "func_key_dest_bsfilter"
    __table_args__: tuple = (
        PrimaryKeyConstraint("func_key_id", "destination_type_id", "filtermember_id"),
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
        Index("func_key_dest_bsfilter__idx__filtermember_id", "filtermember_id"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )  # Keep server default.
    filtermember_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("callfiltermember.id"), nullable=False, primary_key=True
    )

    type: str = "bsfilter"  # String literal

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    filtermember: Mapped["Callfiltermember"] = relationship("Callfiltermember")

    def to_tuple(self) -> tuple[tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (("filter_member_id", self.filtermember_id),)

    @property
    def filter_member_id(self) -> int:
        """The ID of the filter member."""
        return self.filtermember_id

    @filter_member_id.setter
    def filter_member_id(self, value: int) -> None:
        """Set the ID of the filter member."""
        self.filtermember_id = value
