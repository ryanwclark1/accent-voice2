# file: accent_dao/models/rightcallmember.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import CheckConstraint, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .groupfeatures import GroupFeatures
    from .outcall import Outcall
    from .rightcall import RightCall
    from .userfeatures import UserFeatures

RightCallMemberType = Literal["group", "outcall", "user"]


class RightCallMember(Base):
    """Represents a member of a rightcall rule.

    Attributes:
        id: The unique identifier for the rightcall member.
        rightcallid: The ID of the associated rightcall rule.
        type: The type of member ('group', 'outcall', 'user').
        typeval: The ID of the associated entity (group, outcall, or user).
        group: Relationship to GroupFeatures (if type is 'group').
        outcall: Relationship to Outcall (if type is 'outcall').
        user: Relationship to UserFeatures (if type is 'user').
        rightcall: Relationship to RightCall.
        call_permission_id: The ID of the rightcall rule (same as rightcallid).
        user_id: The ID of the user (if type is 'user').

    """

    __tablename__: str = "rightcallmember"
    __table_args__: tuple = (
        CheckConstraint(
            "type IN ('group', 'outcall', 'user')", name="rightcallmember_type_check"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    rightcallid: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # keep
    type: Mapped[RightCallMemberType] = mapped_column(String(64), nullable=False)
    typeval: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default="0"
    )

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            RightCallMember.type == 'group',
            RightCallMember.typeval == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="RightCallMember.typeval",
        viewonly=True,
    )

    outcall: Mapped["Outcall"] = relationship(
        "Outcall",
        primaryjoin="""and_(
            RightCallMember.type == 'outcall',
            RightCallMember.typeval == cast(Outcall.id, String)
        )""",
        foreign_keys="RightCallMember.typeval",
        viewonly=True,
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            RightCallMember.type == 'user',
            RightCallMember.typeval == cast(UserFeatures.id, String)
        )""",
        foreign_keys="RightCallMember.typeval",
        viewonly=True,
    )

    rightcall: Mapped["RightCall"] = relationship(
        "RightCall",
        primaryjoin="RightCall.id == RightCallMember.rightcallid",
        foreign_keys="RightCallMember.rightcallid",
        back_populates="rightcall_members",
    )

    @property
    def call_permission_id(self) -> int:
        """The ID of the rightcall rule."""
        return self.rightcallid

    @call_permission_id.setter
    def call_permission_id(self, value: int) -> None:
        """Set the ID of the rightcall rule."""
        self.rightcallid = value

    @property
    def user_id(self) -> int | None:
        """The ID of the user (if type is 'user')."""
        if self.type == "user":
            return int(self.typeval)
        return None

    @user_id.expression
    def user_id(cls) -> Mapped[int | None]:
        return func.coalesce(
            case((cls.type == "user", func.cast(cls.typeval, Integer)), else_=None),
            None,
        )

    @user_id.setter
    def user_id(self, value: int) -> None:
        """Set the ID of the user."""
        self.type = "user"
        self.typeval = str(value)
