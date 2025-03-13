# file: accent_dao/alchemy/paginguser.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .paging import Paging
    from .userfeatures import UserFeatures


class PagingUser(Base):
    """Represents a user in a paging group.

    Attributes:
        pagingid: The ID of the associated paging group.
        userfeaturesid: The ID of the associated user.
        caller: Indicates if the user is a caller (1) or a member (0).
        paging: Relationship to Paging.
        user: Relationship to UserFeatures.
        paging_id: The ID of the paging group (same as pagingid).
        user_id: The ID of the user (same as userfeaturesid).

    """

    __tablename__: str = "paginguser"
    __table_args__: tuple = (
        PrimaryKeyConstraint("pagingid", "userfeaturesid", "caller"),
        Index("paginguser__idx__pagingid", "pagingid"),
    )

    pagingid: Mapped[int] = mapped_column(
        Integer, ForeignKey("paging.id"), nullable=False, primary_key=True
    )
    userfeaturesid: Mapped[int] = mapped_column(
        Integer, ForeignKey("userfeatures.id"), nullable=False, primary_key=True
    )
    caller: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )

    paging: Mapped["Paging"] = relationship("Paging")
    user: Mapped["UserFeatures"] = relationship("UserFeatures")

    @property
    def paging_id(self) -> int:
        """The ID of the paging group."""
        return self.pagingid

    @paging_id.setter
    def paging_id(self, value: int) -> None:
        """Set the ID of the paging group."""
        self.pagingid = value

    @property
    def user_id(self) -> int:
        """The ID of the user."""
        return self.userfeaturesid

    @user_id.setter
    def user_id(self, value: int) -> None:
        """Set the ID of the user."""
        self.userfeaturesid = value
