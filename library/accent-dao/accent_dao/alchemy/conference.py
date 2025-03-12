# file: accent_dao/models/conference.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, select

from accent_dao.db_manager import Base

from .extension import Extension

if TYPE_CHECKING:
    from .dialaction import Dialaction
    from .func_key_dest_conference import FuncKeyDestConference


class Conference(Base):
    """Represents a conference room.

    Attributes:
        id: The unique identifier for the conference room.
        tenant_uuid: The UUID of the tenant the conference room belongs to.
        name: The name of the conference room.
        preprocess_subroutine: A preprocess subroutine.
        max_users: The maximum number of users allowed in the conference room.
        record: Indicates if the conference room should be recorded.
        pin: The PIN required to join the conference room.
        quiet_join_leave: Indicates if join/leave announcements are quiet.
        announce_join_leave: Indicates if join/leave announcements are made.
        announce_user_count: Indicates if the user count is announced.
        announce_only_user: Indicates if only user announcements are made.
        music_on_hold: The music on hold setting.
        admin_pin: The administrator PIN for the conference room.
        extensions: Relationship to Extension.
        incall_dialactions: Relationship to Dialaction for incall actions.
        incalls: Incall objects associated.
        _dialaction_actions: Relationship to Dialaction.
        func_keys_conference: Relationship to FuncKeyDestConference.
        exten: A computed property for the extension.

    """

    __tablename__: str = "conference"
    __table_args__: tuple = (Index("conference__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    preprocess_subroutine: Mapped[str | None] = mapped_column(String(79), nullable=True)

    max_users: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="50"
    )  # Keep server defaults
    record: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="False"
    )  # Keep server defaults

    pin: Mapped[str | None] = mapped_column(String(80), nullable=True)
    quiet_join_leave: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="False"
    )  # Keep server defaults
    announce_join_leave: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="False"
    )  # Keep server defaults
    announce_user_count: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="False"
    )  # Keep server defaults
    announce_only_user: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="True"
    )  # Keep server defaults
    music_on_hold: Mapped[str | None] = mapped_column(String(128), nullable=True)

    admin_pin: Mapped[str | None] = mapped_column(String(80), nullable=True)

    extensions: Mapped[list["Extension"]] = relationship(
        "Extension",
        primaryjoin="""and_(
            Extension.type == 'conference',
            Extension.typeval == cast(Conference.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    incall_dialactions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.action == 'conference',
            Dialaction.actionarg1 == cast(Conference.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    # This is how you would get the associated incalls, if you really need a list.
    @property
    def incalls(self) -> list[int]:
        """Returns a list of incall identifiers associated with the conference."""
        return [d.incall for d in self.incall_dialactions if d.incall]

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'conference',
            Dialaction.actionarg1 == cast(Conference.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    func_keys_conference: Mapped[list["FuncKeyDestConference"]] = relationship(
        "FuncKeyDestConference", cascade="all, delete-orphan"
    )

    @property
    def exten(self) -> str | None:
        """The conference extension."""
        for extension in self.extensions:
            return extension.exten
        return None

    @exten.setter
    def exten(self, value: str | None) -> None:
        """There is no setter, you can't set the extension directly."""
    # Use a standard property now
    @exten.expression
    def exten(cls) -> Mapped[str]:
        return (
            select(Extension.exten)
            .where(Extension.type == "conference")
            .where(Extension.typeval == func.cast(cls.id, String))
            .scalar_subquery()
        )

