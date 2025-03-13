# file: accent_dao/alchemy/groupfeatures.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    ScalarSelect,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import select

# Fixes added to the import block
from accent_dao.alchemy.callerid import CalleridMode
from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.alchemy.incall import Incall
from accent_dao.alchemy.pickupmember import PickupMember
from accent_dao.helpers.db_manager import Base

from .callerid import Callerid
from .extension import Extension
from .queue import Queue
from .rightcallmember import RightCallMember
from .schedulepath import SchedulePath
from .userfeatures import UserFeatures

if TYPE_CHECKING:
    from .dialaction import Dialaction
    from .func_key_dest_group import FuncKeyDestGroup
    from .func_key_dest_group_member import FuncKeyDestGroupMember
    from .queuemember import QueueMember
    from .rightcall import RightCall
    from .schedule import Schedule  # Corrected import


class GroupFeatures(Base):
    """Represents features for a group."""

    __tablename__: str = "groupfeatures"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint("name"),
        Index("groupfeatures__idx__name", "name"),
        Index("groupfeatures__idx__uuid", "uuid"),
        Index("groupfeatures__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4(), nullable=False
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    transfer_user: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    transfer_call: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    write_caller: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    write_calling: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    ignore_forward: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )
    timeout: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preprocess_subroutine: Mapped[str | None] = mapped_column(String(79), nullable=True)
    mark_answered_elsewhere: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )

    caller_id: Mapped["Callerid"] = relationship(
        "Callerid",
        primaryjoin="""and_(
            Callerid.type == 'group',
            Callerid.typeval == GroupFeatures.id
        )""",
        foreign_keys="Callerid.typeval",
        cascade="all, delete-orphan",
        uselist=False,
    )

    @property
    def caller_id_mode(self) -> str | None:
        """Retrieve the mode of the caller ID."""
        return self.caller_id.mode if self.caller_id else None

    @caller_id_mode.setter
    def caller_id_mode(self, value: CalleridMode) -> None:  # Fix 1
        if self.caller_id:
            self.caller_id.mode = value
        else:
            self.caller_id = Callerid(type="group", mode=value)

    @property
    def caller_id_name(self) -> str | None:
        """Retrieve the caller ID name."""
        return self.caller_id.name if self.caller_id else None

    @caller_id_name.setter
    def caller_id_name(self, value: str | None) -> None:
        if self.caller_id:
            self.caller_id.name = value
        else:
            self.caller_id = Callerid(type="group", name=value)  # type: ignore[assignment]

    extensions: Mapped[list["Extension"]] = relationship(
        "Extension",
        primaryjoin="""and_(
            Extension.type == 'group',
            Extension.typeval == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    incall_dialactions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.action == 'group',
            Dialaction.actionarg1 == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    @property
    def incalls(self) -> list["Incall"]:
        """Incall objects associated."""
        return [d.incall for d in self.incall_dialactions if d.incall]  # Fix 2

    # Removed attribute_mapped_collection
    group_dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'group',
            Dialaction.categoryval == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="Dialaction.categoryval",
        cascade="all, delete-orphan",
    )

    user_queue_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'group',
            not_(QueueMember.interface.startswith('Local/')),
            QueueMember.queue_name == GroupFeatures.name
        )""",
        order_by="QueueMember.position",
        foreign_keys="QueueMember.queue_name",
        cascade="all, delete-orphan",
        passive_updates=False,
    )

    @property
    def users(self) -> list["UserFeatures"]:
        """Retrieve a list of users from the user queue members."""
        return [m.user for m in self.user_queue_members if m.user]

    extension_queue_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'group',
            QueueMember.interface.startswith('Local/'),
            QueueMember.queue_name == GroupFeatures.name
        )""",
        order_by="QueueMember.position",
        foreign_keys="QueueMember.queue_name",
        cascade="all, delete-orphan",
        passive_updates=False,
    )

    queue: Mapped["Queue"] = relationship(
        "Queue",
        primaryjoin="""and_(
            Queue.category == 'group',
            Queue.name == GroupFeatures.name
        )""",
        foreign_keys="Queue.name",
        cascade="all, delete-orphan",
        uselist=False,
        passive_updates=False,
    )

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'group',
            Dialaction.actionarg1 == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    func_keys_group: Mapped[list["FuncKeyDestGroup"]] = relationship(
        "FuncKeyDestGroup", cascade="all, delete-orphan"
    )

    func_keys_group_member: Mapped[list["FuncKeyDestGroupMember"]] = relationship(
        "FuncKeyDestGroupMember", cascade="all, delete-orphan"
    )

    schedule_paths: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.path == 'group',
            SchedulePath.pathid == GroupFeatures.id
        )""",
        foreign_keys="SchedulePath.pathid",
        cascade="all, delete-orphan",
    )

    @property
    def schedules(self) -> list["Schedule"]:
        """Return Schedule objects."""
        return [sp.schedule for sp in self.schedule_paths]

    @schedules.setter
    def schedules(self, value: list["Schedule"]) -> None:
        self.schedule_paths = [
            SchedulePath(path="group", schedule_id=schedule.id, schedule=schedule)  # type: ignore[call-arg]
            for schedule in value
        ]

    rightcall_members: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="""and_(
            RightCallMember.type == 'group',
            RightCallMember.typeval == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="RightCallMember.typeval",
        cascade="all, delete-orphan",
    )

    @property
    def call_permissions(self) -> list["RightCall"]:
        """Retrieve call permissions."""
        return [m.rightcall for m in self.rightcall_members if m.rightcall]

    @call_permissions.setter
    def call_permissions(self, value: list["RightCall"]) -> None:
        self.rightcall_members = [
            RightCallMember(
                type="group", typeval=str(permission.id), rightcall=permission
            )
            for permission in value
        ]

    call_pickup_interceptors: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.category == 'member',
            PickupMember.membertype == 'group',
            PickupMember.memberid == GroupFeatures.id
        )""",
        foreign_keys="PickupMember.memberid",
        cascade="delete, delete-orphan",
    )

    call_pickup_targets: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.category == 'pickup',
            PickupMember.membertype == 'group',
            PickupMember.memberid == GroupFeatures.id
        )""",
        foreign_keys="PickupMember.memberid",
        cascade="delete, delete-orphan",
    )

    @property
    def users_from_call_pickup_user_targets(self) -> list["UserFeatures"]:
        """Retrieve users from call pickup user targets."""
        return [
            p.user
            for p in self.call_pickup_interceptors
            if p.user  # Fix 3
        ]

    @property
    def users_from_call_pickup_group_targets(self) -> list[list[UserFeatures]]:
        """Retrieve users from call pickup group targets."""
        return [
            p.group.members
            for p in self.call_pickup_interceptors
            if p.group and p.group.members  # Fix 3
        ]

    def __init__(self, **kwargs: Any) -> None:  # Added Any Type
        """Initialize a new GroupFeatures object.

        If 'queue' is not provided, it is initialized with default settings.
        """
        queue = kwargs.get("queue")
        if queue is None:
            kwargs["queue"] = Queue(
                name=kwargs.get("name"),  # Use name from kwargs.
                category="group",
                enabled=1,
                musicclass=kwargs.get("music_on_hold"),
                strategy="ringall",
                timeout=15,
                retry=5,
                wrapuptime=0,
                maxlen=0,
                servicelevel=0,
                memberdelay=0,
                weight=0,
                timeoutpriority="conf",
                autofill=1,
                autopause="no",
                setqueueentryvar=1,
                setqueuevar=1,
                queue_youarenext="queue-youarenext",
                queue_thereare="queue-thereare",
                queue_callswaiting="queue-callswaiting",
                queue_holdtime="queue-holdtime",
                queue_minutes="queue-minutes",
                queue_seconds="queue-seconds",
                queue_thankyou="queue-thankyou",
                queue_reporthold="queue-reporthold",
                periodic_announce="queue-periodic-announce",
                announce_frequency=0,
                periodic_announce_frequency=0,
                announce_round_seconds=0,
                announce_holdtime="no",
            )
        super().__init__(**kwargs)

    @hybrid_property
    def enabled(self) -> bool | None:
        """Check if the group is enabled."""
        return self.queue.enabled if self.queue else None  # type: ignore

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set the enabled state of the group."""
        if self.queue:
            self.queue.enabled = value  # type: ignore

    @hybrid_property
    def music_on_hold(self) -> str | None:
        """Get the music on hold setting."""
        return self.queue.musicclass if self.queue else None  # type: ignore

    @music_on_hold.setter
    def music_on_hold(self, value: str | None) -> None:
        """Set the music on hold setting."""
        if self.queue:
            self.queue.musicclass = value  # type: ignore

    @hybrid_property
    def retry_delay(self) -> int | None:
        """Get the retry delay."""
        return self.queue.retry if self.queue else None  # type: ignore

    @retry_delay.setter
    def retry_delay(self, value: int | None) -> None:
        """Set the retry delay."""
        if self.queue:
            self.queue.retry = value  # type: ignore

    @hybrid_property
    def ring_in_use(self) -> int:
        """Get the ring in use setting."""
        return self.queue.ringinuse if self.queue else 0  # type: ignore

    @ring_in_use.setter
    def ring_in_use(self, value: int) -> None:
        """Set the ring in use setting."""
        if self.queue:
            self.queue.ringinuse = value  # type: ignore

    @hybrid_property
    def ring_strategy(self) -> str | None:
        """Get the ring strategy."""
        return self.queue.strategy if self.queue else None  # type: ignore

    @ring_strategy.setter
    def ring_strategy(self, value: str | None) -> None:
        """Set the ring strategy."""
        if self.queue:
            self.queue.strategy = value  # type: ignore

    @hybrid_property
    def user_timeout(self) -> int | None:
        """Get the user timeout."""
        return self.queue.timeout if self.queue else None  # type: ignore

    @user_timeout.setter
    def user_timeout(self, value: int | None) -> None:
        """Set the user timeout."""
        if self.queue:
            self.queue.timeout = value  # type: ignore

    @hybrid_property
    def max_calls(self) -> int | None:
        """Get the maximum calls."""
        return self.queue.maxlen if self.queue else None  # type: ignore

    @max_calls.setter
    def max_calls(self, value: int | None) -> None:
        """Set the maximum calls."""
        if self.queue:
            self.queue.maxlen = value  # type: ignore

    @property
    def fallbacks(self) -> dict[str, "Dialaction"]:
        """Get the fallback dialactions."""
        return self.group_dialactions

    @fallbacks.setter
    def fallbacks(self, dialactions: dict[str, "Dialaction"]) -> None:
        """Set the fallback dialactions."""
        for event in list(self.group_dialactions.keys()):
            if event not in dialactions:
                self.group_dialactions.pop(event, None)

        for event, dialaction in dialactions.items():
            if dialaction is None:
                self.group_dialactions.pop(event, None)
                continue

            if event not in self.group_dialactions:
                dialaction.event = event
                dialaction.category = "group"
                self.group_dialactions[event] = dialaction
            else:
                self.group_dialactions[event].action = dialaction.action
                self.group_dialactions[event].actionarg1 = dialaction.actionarg1
                self.group_dialactions[event].actionarg2 = dialaction.actionarg2

    @hybrid_property
    def mark_answered_elsewhere_bool(self) -> bool:
        """Get the boolean value of mark answered elsewhere."""
        return bool(self.mark_answered_elsewhere)

    @mark_answered_elsewhere_bool.setter
    def mark_answered_elsewhere_bool(self, value: bool) -> None:
        """Set mark_answered_elsewhere from a boolean value."""
        self.mark_answered_elsewhere = int(value is True)

    @property
    def exten(self) -> str | None:
        """Get the extension number."""
        for extension in self.extensions:
            return extension.exten
        return None

    @exten.setter
    def exten(self, value: str) -> None:
        """Set the extension number."""
        # Implementation might depend on how extensions are managed
        # For example, you might need to create or update an Extension object.
        # This is a placeholder.  You'll need to adapt this to the specifics.
        pass

    @exten.expression  # type: ignore[no-redef]
    def exten(cls) -> ScalarSelect[str] | None:
        """Define the database expression for the exten property."""
        return (
            select(Extension.exten)
            .where(Extension.type == "group")
            .where(Extension.typeval == func.cast(cls.id, String))
            .scalar_subquery()
        )
