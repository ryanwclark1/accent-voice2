# file: accent_dao/models/callfiltermember.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Literal

from sqlalchemy import (
    CheckConstraint,
    Enum,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship
from sqlalchemy.sql import and_, select

from accent_dao.helpers.db_manager import Base

from .callfilter import Callfilter

if TYPE_CHECKING:
    from .func_key_dest_bsfilter import FuncKeyDestBSFilter
    from .userfeatures import UserFeatures


CallfiltermemberType = Literal["user"]
GenericBsfilter = Literal["no", "boss", "secretary"]


class Callfiltermember(Base):
    """Represents a member of a call filter.

    Attributes:
        id: The unique identifier for the call filter member.
        callfilterid: The ID of the associated call filter.
        type: The type of member ('user').
        typeval: The ID of the associated entity (e.g., user ID).
        ringseconds: The number of seconds to ring this member.
        priority: The priority of the member.
        bstype: The type of member in a boss-secretary filter ('boss', 'secretary').
        active: Indicates if the member is active.
        callfilter_exten: A computed property for the call filter extension.
        func_keys: Relationship to FuncKeyDestBSFilter.
        user: Relationship to UserFeatures.
        timeout: The timeout for the member.

    """

    __tablename__: str = "callfiltermember"
    __table_args__: tuple = (
        UniqueConstraint("callfilterid", "type", "typeval"),
        CheckConstraint("bstype in ('boss', 'secretary')"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    callfilterid: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    type: Mapped[CallfiltermemberType] = mapped_column(
        Enum("user", name="callfiltermember_type"), nullable=False
    )
    typeval: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default="0"
    )
    ringseconds: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    priority: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    bstype: Mapped[GenericBsfilter] = mapped_column(
        Enum("no", "boss", "secretary", name="generic_bsfilter"), nullable=False
    )
    active: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    callfilter_exten: Mapped[str] = column_property(
        select(Callfilter.exten)
        .where(and_(Callfilter.id == callfilterid, bstype == "secretary"))
        .scalar_subquery()
    )

    func_keys: Mapped[list["FuncKeyDestBSFilter"]] = relationship(
        "FuncKeyDestBSFilter", cascade="all, delete-orphan"
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            Callfiltermember.type == 'user',
            Callfiltermember.typeval == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Callfiltermember.typeval",
    )

    @property
    def timeout(self) -> int | None:
        """The timeout for the member (in seconds)."""
        if self.ringseconds == 0:
            return None
        return self.ringseconds

    @timeout.setter
    def timeout(self, value: int | None) -> None:
        """Set the timeout for the member."""
        if value is None:
            self.ringseconds = 0
        else:
            self.ringseconds = value
