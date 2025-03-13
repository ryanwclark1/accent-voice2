# file: accent_dao/alchemy/conference.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy  # Correct import
from sqlalchemy.ext.hybrid import hybrid_property  # Corrected import
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, select

from accent_dao.helpers.db_manager import Base

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
        incalls: Association proxy to Incall objects associated via dialactions.
        _dialaction_actions: Relationship to Dialaction.
        func_keys_conference: Relationship to FuncKeyDestConference.
        exten: A hybrid property for the extension.

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

    incalls = association_proxy("incall_dialactions", "incall")

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

    @hybrid_property
    def exten(self) -> str | None:
        """Get the conference extension."""
        for extension in self.extensions:
            return extension.exten
        return None

    @exten.setter
    def exten(self, value: str | None) -> None:
        """Raise an error, as you can't set the extension directly."""
        msg = "can't set attribute"
        raise AttributeError(msg)

    @exten.expression  # type: ignore[no-redef]
    def exten(cls) -> Mapped[str | None]:
        """Retrieve the extension identifier for a conference.

        This method constructs a SQL query to select the `exten` field from the
        `Extension` table where the `type` is "conference" and the `typeval`
        matches the string representation of the class's `id`.

        Returns:
            Mapped[str | None]: A scalar subquery that represents the extension
            identifier for the conference.

        """
        return (
            select(Extension.exten)
            .where(Extension.type == "conference")
            .where(Extension.typeval == func.cast(cls.id, String))
            .scalar_subquery()
        )
