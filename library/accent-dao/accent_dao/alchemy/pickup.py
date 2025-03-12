# file: accent_dao/models/pickup.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import cast, func

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .groupfeatures import GroupFeatures
    from .pickupmember import PickupMember
    from .userfeatures import UserFeatures


class Pickup(Base):
    """Represents a call pickup group.

    Attributes:
        id: The unique identifier for the pickup group.
        tenant_uuid: The UUID of the tenant the pickup group belongs to.
        name: The name of the pickup group.
        commented: Indicates if the pickup group is commented out.
        description: A description of the pickup group.
        pickupmember_user_targets: Relationship to PickupMember (user targets).
        user_targets: Users who are targets for call pickup.
    pickupmember_group_targets: Relationship to PickupMember (group targets).
        group_targets: Groups that are targets for call pickup.
    users_from_group_targets: Users from groups that are targets for call pickup.
    pickupmember_user_interceptors: Relationship to PickupMember (user interceptors).
        user_interceptors: Users who can intercept calls.
    pickupmember_group_interceptors: Relationship to PickupMember (group interceptors).
        group_interceptors: Groups that can intercept calls.
        pickupmember_queue_targets: Relationship to PickupMember (queue targets).
        pickupmember_queue_interceptors: Relationship to PickupMember (queue interceptors).
        enabled: Indicates if the pickup group is enabled.

    """

    __tablename__: str = "pickup"
    __table_args__: tuple = (Index("pickup__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    pickupmember_user_targets: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.pickupid == Pickup.id,
            PickupMember.category == 'pickup',
            PickupMember.membertype == 'user'
        )""",
        foreign_keys="PickupMember.pickupid",
        cascade="all, delete-orphan",
    )

    @property
    def user_targets(self) -> list["PickupMember"]:
        return [ptu.user for ptu in self.pickupmember_user_targets if ptu.user]

    @user_targets.setter
    def user_targets(self, value: list["UserFeatures"]) -> None:
        self.pickupmember_user_targets = [
            PickupMember(user=user, category="pickup", membertype="user")
            for user in value
        ]

    pickupmember_group_targets: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.pickupid == Pickup.id,
            PickupMember.category == 'pickup',
            PickupMember.membertype == 'group'
        )""",
        foreign_keys="PickupMember.pickupid",
        cascade="all, delete-orphan",
    )

    @property
    def group_targets(self) -> list["PickupMember"]:
        return [ptg.group for ptg in self.pickupmember_group_targets if ptg.group]

    @group_targets.setter
    def group_targets(self, value: list["GroupFeatures"]) -> None:
        self.pickupmember_group_targets = [
            PickupMember(group=group, category="pickup", membertype="group")
            for group in value
        ]

    @property
    def users_from_group_targets(self) -> list["GroupFeatures"]:
        return [gt.users for gt in self.group_targets if gt.users]

    pickupmember_user_interceptors: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.pickupid == Pickup.id,
            PickupMember.category == 'member',
            PickupMember.membertype == 'user'
        )""",
        foreign_keys="PickupMember.pickupid",
        cascade="all, delete-orphan",
    )

    @property
    def user_interceptors(self) -> list["PickupMember"]:
        return [ptu.user for ptu in self.pickupmember_user_interceptors if ptu.user]

    @user_interceptors.setter
    def user_interceptors(self, value: list["UserFeatures"]) -> None:
        self.pickupmember_user_interceptors = [
            PickupMember(user=user, category="member", membertype="user")
            for user in value
        ]

    pickupmember_group_interceptors: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.pickupid == Pickup.id,
            PickupMember.category == 'member',
            PickupMember.membertype == 'group'
        )""",
        foreign_keys="PickupMember.pickupid",
        cascade="all, delete-orphan",
    )

    @property
    def group_interceptors(self) -> list["PickupMember"]:
        return [ptg.group for ptg in self.pickupmember_group_interceptors if ptg.group]

    @group_interceptors.setter
    def group_interceptors(self, value: list["GroupFeatures"]) -> None:
        self.pickupmember_group_interceptors = [
            PickupMember(group=group, category="member", membertype="group")
            for group in value
        ]

    pickupmember_queue_targets: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.pickupid == Pickup.id,
            PickupMember.category == 'pickup',
            PickupMember.membertype == 'queue'
        )""",
        foreign_keys="PickupMember.pickupid",
        cascade="all, delete-orphan",
    )

    pickupmember_queue_interceptors: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.pickupid == Pickup.id,
            PickupMember.category == 'member',
            PickupMember.membertype == 'queue'
        )""",
        foreign_keys="PickupMember.pickupid",
        cascade="all, delete-orphan",
    )

    @property
    def enabled(self) -> bool | None:
        """Indicates if the pickup group is enabled."""
        if self.commented is None:
            return None
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        """Enable or disables the pickup group."""
        self.commented = int(not value) if value is not None else None

    @enabled.expression
    def enabled(cls) -> Mapped[bool]:
        return func.not_(cast(cls.commented, Boolean))
