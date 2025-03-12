# file: accent_dao/models/func_key_dest_custom.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .func_key import FuncKey


class FuncKeyDestCustom(Base):
    """Represents a function key destination for a custom extension.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 10).
        exten: The custom extension.
        type: The type of destination ('custom').
        func_key: Relationship to FuncKey.

    """

    DESTINATION_TYPE_ID: int = 10

    __tablename__: str = "func_key_dest_custom"
    __table_args__: tuple = (
        PrimaryKeyConstraint("func_key_id", "destination_type_id"),
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )  # Kept server default
    exten: Mapped[str] = mapped_column(String(40), nullable=False)

    type: str = "custom"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )

    def to_tuple(self) -> tuple[tuple[str, str]]:
        """Return a tuple representation of the destination."""
        return (("exten", self.exten),)
