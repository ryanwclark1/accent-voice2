# file: accent_dao/models/switchboard.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.uuid import new_uuid

from .dialaction import Dialaction
from .switchboard_member_user import SwitchboardMemberUser

if TYPE_CHECKING:
    from .moh import MOH


class Switchboard(Base):
    """Represents a switchboard configuration.

    Attributes:
        uuid: The unique identifier for the switchboard.
        tenant_uuid: The UUID of the tenant the switchboard belongs to.
        name: The name of the switchboard.
        hold_moh_uuid: The UUID of the MOH setting for hold music.
        queue_moh_uuid: The UUID of the MOH setting for queue music.
        timeout: The timeout for the switchboard.
        incall_dialactions: Relationship to Dialaction for incall actions.
        incalls: Incall objects associated.
        switchboard_dialactions: Relationship to Dialaction, mapped by event.
        _dialaction_actions: Relationship to Dialaction.
        switchboard_member_users: Relationship to SwitchboardMemberUser.
        user_members: Relationship to users.
        _queue_moh: Relationship to MOH (queue music).
        _hold_moh: Relationship to MOH (hold music).
        queue_music_on_hold: The name of the queue music on hold setting.
    waiting_room_music_on_hold: The name of the waiting room music on hold setting.
        fallbacks: The fallback dialactions.

    """

    __tablename__: str = "switchboard"
    __table_args__: tuple = (
        Index("switchboard__idx__tenant_uuid", "tenant_uuid"),
        Index("switchboard__idx__hold_moh_uuid", "hold_moh_uuid"),
        Index("switchboard__idx__queue_moh_uuid", "queue_moh_uuid"),
    )

    uuid: Mapped[str] = mapped_column(
        String(38), nullable=False, default=new_uuid, primary_key=True
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    hold_moh_uuid: Mapped[str | None] = mapped_column(
        String(38), ForeignKey("moh.uuid", ondelete="SET NULL"), nullable=True
    )
    queue_moh_uuid: Mapped[str | None] = mapped_column(
        String(38), ForeignKey("moh.uuid", ondelete="SET NULL"), nullable=True
    )
    timeout: Mapped[int | None] = mapped_column(Integer, nullable=True)

    incall_dialactions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.action == 'switchboard',
            Dialaction.actionarg1 == Switchboard.uuid
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    @property
    def incalls(self) -> list["Dialaction"]:
        """Return a list of incall Dialaction objects."""
        return [d.incall for d in self.incall_dialactions if d.incall]

    # Removed collection_class
    switchboard_dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(Dialaction.category == 'switchboard',
                            Dialaction.categoryval == Switchboard.uuid)""",
        cascade="all, delete-orphan",
        foreign_keys="Dialaction.categoryval",
    )

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'switchboard',
            Dialaction.actionarg1 == Switchboard.uuid
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    switchboard_member_users: Mapped[list["SwitchboardMemberUser"]] = relationship(
        "SwitchboardMemberUser",
        primaryjoin="""SwitchboardMemberUser.switchboard_uuid == Switchboard.uuid""",
        cascade="all, delete-orphan",
    )

    @property
    def user_members(self) -> list["SwitchboardMemberUser"]:
        """Return a list of user members associated with the switchboard."""
        return [smu.user for smu in self.switchboard_member_users if smu.user]

    @user_members.setter
    def user_members(self, value: list["SwitchboardMemberUser"]) -> None:
        """Set the user members for the switchboard."""
        self.switchboard_member_users = [
            SwitchboardMemberUser(user=user) for user in value
        ]

    _queue_moh: Mapped["MOH"] = relationship(
        "MOH", primaryjoin="Switchboard.queue_moh_uuid == MOH.uuid"
    )
    _hold_moh: Mapped["MOH"] = relationship(
        "MOH", primaryjoin="Switchboard.hold_moh_uuid == MOH.uuid"
    )

    @property
    def queue_music_on_hold(self) -> str | None:
        """The name of the queue music on hold setting."""
        return self._queue_moh.name if self._queue_moh else None

    @property
    def waiting_room_music_on_hold(self) -> str | None:
        """The name of the waiting room music on hold setting."""
        return self._hold_moh.name if self._hold_moh else None

    @property
    def fallbacks(self) -> dict[str, "Dialaction"]:
        """Return the fallback dialactions for the switchboard."""
        return self.switchboard_dialactions

    @fallbacks.setter
    def fallbacks(self, dialactions: dict[str, "Dialaction"]) -> None:
        """Set the fallback dialactions for the switchboard."""
        for event in list(self.switchboard_dialactions.keys()):
            if event not in dialactions:
                self.switchboard_dialactions.pop(event, None)

        for event, dialaction in dialactions.items():
            self._set_dialaction(event, dialaction)

    def _set_dialaction(self, event: str, dialaction: Dialaction | None) -> None:
        """Set a dialaction for a specific event."""
        if dialaction is None:
            self.switchboard_dialactions.pop(event, None)
            return

        if event not in self.switchboard_dialactions:
            dialaction.event = event
            dialaction.category = "switchboard"
            self.switchboard_dialactions[event] = dialaction
        else:
            self.switchboard_dialactions[event].action = dialaction.action
            self.switchboard_dialactions[event].actionarg1 = dialaction.actionarg1
            self.switchboard_dialactions[event].actionarg2 = dialaction.actionarg2
