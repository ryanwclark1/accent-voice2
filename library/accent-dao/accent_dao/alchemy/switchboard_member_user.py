# file: accent_dao/models/switchboard_member_user.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .switchboard import Switchboard
    from .userfeatures import UserFeatures


class SwitchboardMemberUser(Base):
    """Represents a user who is a member of a switchboard.

    Attributes:
        switchboard_uuid: The UUID of the associated switchboard.
        user_uuid: The UUID of the associated user.
        switchboard: Relationship to Switchboard.
        user: Relationship to UserFeatures.

    """

    __tablename__: str = "switchboard_member_user"
    __table_args__: tuple = (
        PrimaryKeyConstraint("switchboard_uuid", "user_uuid"),
        Index("switchboard_member_user__idx__switchboard_uuid", "switchboard_uuid"),
        Index("switchboard_member_user__idx__user_uuid", "user_uuid"),
    )

    switchboard_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("switchboard.uuid", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    user_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("userfeatures.uuid", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    switchboard: Mapped["Switchboard"] = relationship("Switchboard")
    user: Mapped["UserFeatures"] = relationship("UserFeatures")
