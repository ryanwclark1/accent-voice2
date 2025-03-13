# file: accent_dao/alchemy/paging.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from accent_dao.helpers.db_manager import Base

from .paginguser import PagingUser

if TYPE_CHECKING:
    from .func_key_dest_paging import FuncKeyDestPaging
    from .userfeatures import UserFeatures


class Paging(Base):
    """Represents a paging group.

    Attributes:
        id: The unique identifier for the paging group.
        tenant_uuid: The UUID of the tenant the paging group belongs to.
        number: The number of the paging group.
        name: The name of the paging group.
        duplex: Indicates if duplex communication is enabled.
        ignore: Indicates if forwarding should be ignored.
        record: Indicates if calls should be recorded.
        quiet: Indicates if caller notification should be quiet.
        timeout: The timeout for paging.
        announcement_file: The announcement file.
        announcement_play: Indicates if the announcement should be played.
        announcement_caller: Indicates if the caller should be announced.
        commented: Indicates if the paging group is commented out.
        description: A description of the paging group.
        paging_members: Relationship to PagingUser (members).
        users_member: The users of the paging group.
        paging_callers: Relationship to PagingUser (callers).
        users_caller: The callers that can call the paging group.
        func_keys: Relationship to FuncKeyDestPaging.
        enabled: Indicates if the paging group is enabled.
        duplex_bool: Boolean representation of duplex.
        record_bool: Boolean representation of record.
        ignore_forward: Boolean representation of ignore.
        caller_notification: Boolean representation of caller notification.
        announce_caller: Boolean representation of announce caller.
        announce_sound: The announcement sound.

    """

    __tablename__: str = "paging"
    __table_args__: tuple = (Index("paging__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    number: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    duplex: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    ignore: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    record: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    quiet: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    timeout: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="30"
    )  # Keep server default
    announcement_file: Mapped[str | None] = mapped_column(String(64), nullable=True)
    announcement_play: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    announcement_caller: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    paging_members: Mapped[list["PagingUser"]] = relationship(
        "PagingUser",
        primaryjoin="""and_(
            PagingUser.pagingid == Paging.id,
            PagingUser.caller == 0
        )""",
        cascade="all, delete-orphan",
    )

    @property
    def users_member(self) -> list["PagingUser"]:
        return [pm.user for pm in self.paging_members]

    @users_member.setter
    def users_member(self, value: list["UserFeatures"]) -> None:
        self.paging_members = [
            PagingUser(user=user, caller=0) for user in value
        ]  # Corrected

    paging_callers: Mapped[list["PagingUser"]] = relationship(
        "PagingUser",
        primaryjoin="""and_(
            PagingUser.pagingid == Paging.id,
            PagingUser.caller == 1
        )""",
        cascade="all, delete-orphan",
    )

    @property
    def users_caller(self) -> list["PagingUser"]:
        return [pc.user for pc in self.paging_callers]

    @users_caller.setter
    def users_caller(self, value: list["UserFeatures"]) -> None:
        self.paging_callers = [
            PagingUser(user=user, caller=1) for user in value
        ]  # Corrected

    func_keys: Mapped[list["FuncKeyDestPaging"]] = relationship(
        "FuncKeyDestPaging", cascade="all, delete-orphan"
    )

    @property
    def enabled(self) -> bool:
        """Indicates if the paging group is enabled."""
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disables the paging group."""
        self.commented = int(not value)

    @enabled.expression
    def enabled(cls) -> Mapped[bool]:
        return func.not_(cast(cls.commented, Boolean))

    @property
    def duplex_bool(self) -> bool:
        """Boolean representation of duplex."""
        return self.duplex == 1

    @duplex_bool.setter
    def duplex_bool(self, value: bool) -> None:
        """Set the duplex setting."""
        self.duplex = int(value)

    @duplex_bool.expression
    def duplex_bool(cls) -> Mapped[bool]:
        return func.cast(cls.duplex, Boolean)

    @property
    def record_bool(self) -> bool:
        """Boolean representation of record."""
        return self.record == 1

    @record_bool.setter
    def record_bool(self, value: bool) -> None:
        """Set the record setting."""
        self.record = int(value)

    @record_bool.expression
    def record_bool(cls) -> Mapped[bool]:
        return func.cast(cls.record, Boolean)

    @property
    def ignore_forward(self) -> bool:
        """Boolean representation of ignore forward."""
        return self.ignore == 1

    @ignore_forward.setter
    def ignore_forward(self, value: bool) -> None:
        """Set the ignore forward setting."""
        self.ignore = int(value)

    @ignore_forward.expression
    def ignore_forward(cls) -> Mapped[bool]:
        return func.cast(cls.ignore, Boolean)

    @property
    def caller_notification(self) -> bool:
        """Boolean representation of caller notification."""
        return self.quiet == 0

    @caller_notification.setter
    def caller_notification(self, value: bool) -> None:
        """Set the caller notification setting."""
        self.quiet = int(not value)

    @caller_notification.expression
    def caller_notification(cls) -> Mapped[bool]:
        return func.not_(cast(cls.quiet, Boolean))

    @property
    def announce_caller(self) -> bool:
        """Boolean representation of announce caller."""
        return self.announcement_caller == 0

    @announce_caller.setter
    def announce_caller(self, value: bool) -> None:
        """Set the announce caller setting."""
        self.announcement_caller = int(not value)

    @announce_caller.expression
    def announce_caller(cls) -> Mapped[bool]:
        return func.not_(cast(cls.announcement_caller, Boolean))

    @property
    def announce_sound(self) -> str | None:
        """The announcement sound file."""
        return self.announcement_file

    @announce_sound.setter
    def announce_sound(self, value: str | None) -> None:
        """Set the announcement sound file."""
        self.announcement_play = int(value is not None)
        self.announcement_file = value
