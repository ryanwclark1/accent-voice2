# file: accent_dao/models/func_key_dest_user.py
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
    from .func_key import FuncKey
    from .userfeatures import UserFeatures


class FuncKeyDestUser(Base):
    """Represents a function key destination for a user.

    Attributes:
        func_key_id: The ID of the associated function key.
        user_id: The ID of the associated user.
        destination_type_id: The ID of the destination type (fixed to 1).
        type: The type of destination ('user').
        func_key: Relationship to FuncKey.
        userfeatures: Relationship to UserFeatures.

    """

    DESTINATION_TYPE_ID: int = 1

    __tablename__: str = "func_key_dest_user"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("userfeatures.id"), primary_key=True
    )
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )

    type: str = "user"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    userfeatures: Mapped["UserFeatures"] = relationship("UserFeatures")

    @classmethod
    def for_user(cls, func_key: "FuncKey", user: "UserFeatures") -> "FuncKeyDestUser":
        """Create a new FuncKeyDestUser for a given function key and user."""
        destination = cls(func_key=func_key, userfeatures=user)
        return destination

    def to_tuple(self) -> tuple[tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (("user_id", self.user_id),)
