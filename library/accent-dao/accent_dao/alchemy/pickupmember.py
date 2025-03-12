# file: accent_dao/models/pickupmember.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .groupfeatures import GroupFeatures
    from .userfeatures import UserFeatures


PickupCategory = Literal["member", "pickup"]
PickupMembertype = Literal["group", "queue", "user"]


class PickupMember(Base):
    """Represents a member of a pickup group or a target for pickup.

    Attributes:
        pickupid: The ID of the associated pickup group.
        category: The category of membership ('member' or 'pickup').
        membertype: The type of member ('group', 'queue', 'user').
        memberid: The ID of the associated member entity.
        user: Relationship to UserFeatures (if membertype is 'user').
        group: Relationship to GroupFeatures (if membertype is 'group').
        users_from_group: Users associated via group membership.

    """

    __tablename__: str = "pickupmember"

    pickupid: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    category: Mapped[PickupCategory] = mapped_column(
        Enum("member", "pickup", name="pickup_category"),
        nullable=False,
        autoincrement=False,
        primary_key=True,
    )
    membertype: Mapped[PickupMembertype] = mapped_column(
        Enum("group", "queue", "user", name="pickup_membertype"),
        nullable=False,
        autoincrement=False,
        primary_key=True,
    )
    memberid: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            PickupMember.membertype == 'user',
            PickupMember.memberid == UserFeatures.id
        )""",
        foreign_keys="PickupMember.memberid",
    )

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            PickupMember.membertype == 'group',
            PickupMember.memberid == GroupFeatures.id
        )""",
        foreign_keys="PickupMember.memberid",
    )

    @property
    def users_from_group(self) -> list["UserFeatures"]:
        return (
            self.group.users
            if self.group is not None and hasattr(self.group, "users")
            else []
        )
