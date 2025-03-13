# file: accent_dao/alchemy/func_key_dest_paging.py  # noqa: ERA001
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

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .func_key import FuncKey
    from .paging import Paging


class FuncKeyDestPaging(Base):
    """Represents a function key destination for a paging group.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 9).
        paging_id: The ID of the associated paging group.
        type: The type of destination ('paging').
        func_key: Relationship to FuncKey.
        paging: Relationship to Paging.

    """

    DESTINATION_TYPE_ID: int = 9

    __tablename__: str = "func_key_dest_paging"
    __table_args__: tuple = (
        PrimaryKeyConstraint("func_key_id", "destination_type_id", "paging_id"),
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
        Index("func_key_dest_paging__idx__paging_id", "paging_id"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )
    paging_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("paging.id"), primary_key=True
    )

    type: str = "paging"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    paging: Mapped["Paging"] = relationship("Paging")

    def to_tuple(self) -> tuple[tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (("paging_id", self.paging_id),)
