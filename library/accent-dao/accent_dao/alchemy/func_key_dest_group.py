# file: accent_dao/models/func_key_dest_group.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .func_key import FuncKey
    from .groupfeatures import GroupFeatures


class FuncKeyDestGroup(Base):
    """Represents a function key destination for a group.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 2).
        group_id: The ID of the associated group.
        type: The type of destination ('group').
        func_key: Relationship to FuncKey.
        groupfeatures: Relationship to GroupFeatures.

    """

    DESTINATION_TYPE_ID: int = 2

    __tablename__: str = "func_key_dest_group"
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
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("groupfeatures.id"), primary_key=True
    )

    type: str = "group"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    groupfeatures: Mapped["GroupFeatures"] = relationship("GroupFeatures")

    def to_tuple(self) -> tuple[tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (("group_id", self.group_id),)
