# file: accent_dao/alchemy/rightcall.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import case, func
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.expression import cast as sql_cast

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.exception import InputError

from .rightcallexten import RightCallExten

if TYPE_CHECKING:
    from .rightcallmember import RightCallMember

RightCallMode = Literal["allow", "deny"]


class RightCall(Base):
    """Represents a rightcall (call permission) rule.

    Attributes:
        id: The unique identifier for the right
        tenant_uuid: The UUID of the tenant the rule belongs to.
        name: The name of the rule.
        passwd: The password associated with the rule.
        authorization: The authorization mode (0 for deny, 1 for allow).
        commented: Indicates if the rule is commented out.
        description: A description of the rule.
        rightcallextens: Relationship to RightCallExten.
        rightcall_members: Relationship to RightCallMember.
        rightcall_outcalls: Relationship to RightCallMember for outcall type.
        outcalls: The outcalls the permission is assigned.
        rightcall_groups: Relationship to RightCallMember group type.
        groups: The groups the permission is assigned.
        rightcall_users: Relationship to RightCallMember user types.
        users: The users the permission is assigned.
        password: The password (null if empty).
        mode: The authorization mode ('allow' or 'deny').
        enabled: Indicates if the rule is enabled.
        extensions: The extensions associated with the rule.

    """

    __tablename__: str = "rightcall"
    __table_args__: tuple = (
        UniqueConstraint("name", "tenant_uuid"),
        Index("rightcall__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    passwd: Mapped[str] = mapped_column(String(40), nullable=False, server_default="")
    authorization: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    rightcallextens: Mapped[list["RightCallExten"]] = relationship(
        "RightCallExten", cascade="all, delete-orphan"
    )

    rightcall_members: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="RightCallMember.rightcallid == RightCall.id",
        foreign_keys="RightCallMember.rightcallid",
        cascade="all, delete-orphan",
        back_populates="rightcall",
    )

    rightcall_outcalls: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="""and_(
            RightCallMember.rightcallid == RightCall.id,
            RightCallMember.type == 'outcall'
        )""",
        foreign_keys="RightCallMember.rightcallid",
        viewonly=True,
    )

    @property
    def outcalls(self) -> list["RightCallMember"]:
        """Retrieve a list of RightCallMember instances associated with this RightCall.

        Returns:
            list[RightCallMember]: A list of RightCallMember instances that are
            associated with this RightCall.

        """
        return [rco for rco in self.rightcall_outcalls if rco.outcall]

    rightcall_groups: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="""and_(
            RightCallMember.rightcallid == RightCall.id,
            RightCallMember.type == 'group'
        )""",
        foreign_keys="RightCallMember.rightcallid",
        viewonly=True,
    )

    @property
    def groups(self) -> list["RightCallMember"]:
        """Retrieve a list of RightCallMember groups associated with this instance.

        Returns:
            list[RightCallMember]: A list of RightCallMember groups.

        """
        return [rcg for rcg in self.rightcall_groups if rcg.group]

    rightcall_users: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="""and_(
            RightCallMember.rightcallid == RightCall.id,
            RightCallMember.type == 'user'
        )""",
        foreign_keys="RightCallMember.rightcallid",
        viewonly=True,
    )

    @property
    def users(self) -> list["RightCallMember"]:
        """Retrieve a list of RightCallMember users associated with this instance.

        Returns:
            list[RightCallMember]: A list of RightCallMember users.

        """
        return [rcu for rcu in self.rightcall_users if rcu.user]

    @hybrid_property
    def password(self) -> str | None:
        """The password (null if empty)."""
        if self.passwd == "":
            return None
        return self.passwd

    @password.setter
    def password(self, value: str | None) -> None:
        """Set the password."""
        if value is None:
            self.passwd = ""
        else:
            self.passwd = value

    @password.expression
    def password(self) -> ClauseElement:
        """Return the password if it is not an empty string, otherwise return None.

        Compare the password attribute of the class with an empty string. If they
        are equal, it returns None; otherwise, it returns the password.

        Returns:
            ClauseElement: SQL expression representing the password logic

        """
        return func.nullif(self.passwd, "")

    @hybrid_property
    def mode(self) -> RightCallMode:
        """The authorization mode ('allow' or 'deny')."""
        if self.authorization == 1:
            return "allow"
        return "deny"

    @mode.setter
    def mode(self, value: RightCallMode) -> None:
        """Set the authorization mode."""
        if value == "allow":
            self.authorization = 1
        elif value == "deny":
            self.authorization = 0
        else:
            error_msg = (
                f"cannot set mode to {value}. Only 'allow' or 'deny' are authorized"
            )
            raise InputError(error_msg)

    @mode.expression
    def mode(self) -> ClauseElement:
        """Determine the mode of the RightCall based on the authorization status.

        Returns:
            ClauseElement: SQL expression representing the mode logic

        """
        # Create a dictionary mapping for the case expression
        case_dict = {self.authorization == 1: "allow"}
        return func.coalesce(
            case(case_dict, else_="deny"),
            "deny",
        )

    @hybrid_property
    def enabled(self) -> bool:
        """Indicates if the rule is enabled."""
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disables the rule."""
        self.commented = int(not value)

    @enabled.expression
    def enabled(self) -> ClauseElement:
        """Determine if the instance is enabled based on the 'commented' attribute.

        Returns:
            ClauseElement: SQL expression representing the enabled logic

        """
        return sql_cast(self.commented == 0, Boolean)

    @property
    def extensions(self) -> list[str]:
        """The extensions associated with the rule."""
        return [rightcallexten.exten for rightcallexten in self.rightcallextens]

    @extensions.setter
    def extensions(self, values: list[str]) -> None:
        """Set the extensions associated with the rule."""
        old_rightcallextens = {
            rightcallexten.exten: rightcallexten
            for rightcallexten in self.rightcallextens
        }
        self.rightcallextens = []
        for value in set(values):
            if value in old_rightcallextens:
                self.rightcallextens.append(old_rightcallextens[value])
            else:
                self.rightcallextens.append(
                    RightCallExten(rightcallid=self.id, exten=value)
                )
