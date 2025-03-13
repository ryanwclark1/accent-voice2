# file: accent_dao/alchemy/groupfeatures.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    ScalarSelect,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import cast, select

from accent_dao.helpers.db_manager import Base

from .callerid import Callerid
from .extension import Extension
from .queue import Queue
from .rightcallmember import RightCallMember
from .schedulepath import SchedulePath

if TYPE_CHECKING:
    from accent_dao.alchemy.func_key_dest_group import FuncKeyDestGroup
    from accent_dao.alchemy.func_key_dest_group_member import FuncKeyDestGroupMember

    from .dialaction import Dialaction
    from .pickup import Pickup
    from .pickupmember import PickupMember
    from .queuemember import QueueMember
    from .rightcall import RightCall


class GroupFeatures(Base):
    """Represents features for a group.

    Attributes:
        id: The unique identifier for the group features.
        uuid: A unique UUID for the group.
        tenant_uuid: The UUID of the tenant the group belongs to.
        name: The name of the group.
        label: The label (display name) of the group.
        transfer_user: Indicates if call transfer to users is allowed.
        transfer_call: Indicates if call transfer is allowed.
        write_caller: Indicates if caller information can be written.
        write_calling: Indicates if calling information can be written.
        ignore_forward: Indicates if call forwarding should be ignored.
        timeout: The timeout for the group.
        preprocess_subroutine: A preprocess subroutine.
        mark_answered_elsewhere: Flag to mark call answered by another member.
        caller_id: Relationship to Callerid.
        caller_id_mode: The caller ID mode.
        caller_id_name: The caller ID name.
        extensions: Relationship to Extension.
        incall_dialactions: Relationship to Dialaction for incall actions.
        incalls: Associated incall objects, if any.
        group_dialactions: Relationship to Dialaction, mapped by event.
        user_queue_members: Relationship to QueueMember for user members.
        users: The user that belongs to the group.
        extension_queue_members: Relationship to QueueMember for extension members.
        queue: Relationship to Queue.
        _dialaction_actions: Relationship to Dialaction.
        enabled: Indicates if the group is enabled.
        music_on_hold: The music on hold setting.
        retry_delay: The retry delay.
        ring_in_use: Indicates if the ring-in-use setting is enabled.
        ring_strategy: The ring strategy.
        user_timeout: The user timeout.
        max_calls: The maximum number of calls.
        func_keys_group: Relationship to FuncKeyDestGroup.
        func_keys_group_member: Relationship to FuncKeyDestGroupMember.
        schedule_paths: Relationship to SchedulePath.
        schedules: Schedules for the group.
        rightcall_members: Relationship to RightCallMember.
        call_permissions: Call permissions for the group.
    call_pickup_interceptors: Relationship to users that can intercept call pickups.
    call_pickup_targets: Relationship to users that can be the targets for call pickups.
    call_pickup_interceptor_pickups: Relationship to pickup groups that the users
        are interceptors for.
    users_from_call_pickup_user_targets:
    users_from_call_pickup_group_targets:
        fallbacks: The fallback dialactions.
        mark_answered_elsewhere_bool: Boolean version of mark_answered_elsewhere.
        exten: The extension number.

    """

    __tablename__: str = "groupfeatures"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
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
        """Retrieve the mode of the caller ID.

        Returns:
            str | None: The mode of the caller ID if it exists, otherwise None.

        """
        return self.caller_id.mode if self.caller_id else None

    @caller_id_mode.setter
    def caller_id_mode(self, value: str) -> None:
        if self.caller_id:
            self.caller_id.mode = value
        else:
            self.caller_id = Callerid(type="group", mode=value)

    @property
    def caller_id_name(self) -> str | None:
        """Retrieves the caller ID name.

        Returns:
            str | None: The name of the caller ID if it exists, otherwise None.

        """
        return self.caller_id.name if self.caller_id else None

    @caller_id_name.setter
    def caller_id_name(self, value: str | None) -> None:
        if self.caller_id:
            self.caller_id.name = value
        else:
            self.caller_id = Callerid(type="group", name=value)

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
    def incalls(self) -> list["Dialaction"]:
        """Incall objects associated."""
        return [d.incall for d in self.incall_dialactions if d.incall]

    # Removed attribute_mapped_collection
    group_dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'group',
            Dialaction.categoryval == cast(GroupFeatures.id, String)
        )""",
        cascade="all, delete-orphan",
        foreign_keys="Dialaction.categoryval",
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
    def users(self) -> list["QueueMember"]:
        """Retrieve a list of users from the user queue members.

        Returns:
            list[QueueMember]: A list of users who are members of the user queue.

        """
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

    # These all now use properties to access the attributes of the queue object.
    @property
    def enabled(self) -> bool | None:
        """Check if the queue is enabled.

        Returns:
            bool | None: True if the queue is enabled, False if it is disabled,
                         or None if the queue does not exist.

        """
        return self.queue.enabled if self.queue else None

    @property
    def music_on_hold(self) -> str | None:
        """Retrieve the music on hold class for the queue.

        Returns:
            str | None: The music class if the queue exists, otherwise None.

        """
        return self.queue.musicclass if self.queue else None

    @property
    def retry_delay(self) -> int | None:
        """Returns the retry delay for the queue.

        If the queue is available, it returns the retry delay value.
        Otherwise, it returns None.

        Returns:
            int | None: The retry delay value if the queue is available, otherwise None.

        """
        return self.queue.retry if self.queue else None

    @property
    def ring_in_use(self) -> int:
        """Returns the number of rings currently in use.

        If the queue is not available, it returns 0.

        Returns:
            int: The number of rings in use or 0 if the queue is not available.

        """
        return self.queue.ringinuse if self.queue else 0

    @property
    def ring_strategy(self) -> str | None:
        """Returns the ring strategy of the queue.

        If the queue is not set, returns None.

        Returns:
            str | None: The ring strategy of the queue if available, otherwise None.

        """
        return self.queue.strategy if self.queue else None

    @property
    def user_timeout(self) -> int | None:
        """Retrieve the timeout value for the user from the queue.

        Returns:
            int | None: The timeout value if the queue exists, otherwise None.

        """
        return self.queue.timeout if self.queue else None

    @property
    def max_calls(self) -> int | None:
        """Returns the maximum number of calls that can be stored in the queue.

        Returns:
            int | None: The maximum length of the queue if it exists, otherwise None.

        """
        return self.queue.maxlen if self.queue else None

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
    def schedules(self) -> list[SchedulePath]:
        """Retrieve a list of schedules from the schedule paths.

        Returns:
            list[SchedulePath]: A list of SchedulePath objects.

        """
        return [sp.schedule for sp in self.schedule_paths]

    @schedules.setter
    def schedules(self, value: list["SchedulePath"]) -> None:
        self.schedule_paths = [
            SchedulePath(path="group", schedule_id=schedule.id, schedule=schedule)
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
    def call_permissions(self) -> list["RightCallMember"]:
        """Retrieve list of RightCallMember instances associated with current object.

        Returns:
            list[RightCallMember]: A list of RightCallMember instances where the
                rightcall attribute is not None.

        """
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

    call_pickup_interceptor_pickups: Mapped[list["Pickup"]] = relationship(
        "Pickup",
        primaryjoin="""and_(
            PickupMember.category == 'member',
            PickupMember.membertype == 'group',
            PickupMember.memberid == GroupFeatures.id
        )""",
        secondary="join(PickupMember, Pickup, Pickup.id == PickupMember.pickupid)",
        secondaryjoin="Pickup.id == PickupMember.pickupid",
        foreign_keys="PickupMember.pickupid,PickupMember.memberid",
        viewonly=True,
    )

    @property
    def users_from_call_pickup_user_targets(self) -> list:
        """Retrieve users from call pickup user targets."""
        return [
            p.user_targets
            for p in self.call_pickup_interceptor_pickups
            if p.user_targets
        ]

    @property
    def users_from_call_pickup_group_targets(self) -> list:
        """Retrieve users from call pickup group targets."""
        return [
            p.users_from_group_targets
            for p in self.call_pickup_interceptor_pickups
            if p.users_from_group_targets
        ]

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the GroupFeatures object, creating Queue if one doesn't exist."""
        retry = kwargs.pop("retry_delay", 5)
        ring_in_use = kwargs.pop("ring_in_use", True)
        strategy = kwargs.pop("ring_strategy", "ringall")
        timeout = kwargs.pop("user_timeout", 15)
        musicclass = kwargs.pop("music_on_hold", None)
        enabled = kwargs.pop("enabled", True)
        max_calls = kwargs.pop("max_calls", 0)
        super().__init__(**kwargs)
        if not self.queue:
            self.queue = Queue(
                retry=retry,
                ring_in_use=int(ring_in_use),  # Convert to integer
                strategy=strategy,
                timeout=timeout,
                musicclass=musicclass,
                enabled=int(enabled),  # Convert to integer.
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
                wrapuptime=0,
                maxlen=max_calls,
                memberdelay=0,
                weight=0,
                category="group",
                autofill=1,
                announce_position="no",
            )

    @property
    def fallbacks(self) -> dict[str, "Dialaction"]:
        """The fallback dialactions for the group."""
        return self.group_dialactions

    # Note: fallbacks[key] = Dialaction() doesn't pass in this method
    @fallbacks.setter
    def fallbacks(self, dialactions: dict[str, "Dialaction"]) -> None:
        """Set the fallback dialactions for the group.  Handles None values."""
        for event in list(self.group_dialactions.keys()):
            if event not in dialactions:
                self.group_dialactions.pop(event, None)

        for event, dialaction in dialactions.items():
            if dialaction is None:
                self.group_dialactions.pop(event, None)
                continue

            if event not in self.group_dialactions:
                dialaction.category = "group"
                dialaction.event = event
                self.group_dialactions[event] = dialaction

            self.group_dialactions[event].action = dialaction.action
            self.group_dialactions[event].actionarg1 = dialaction.actionarg1
            self.group_dialactions[event].actionarg2 = dialaction.actionarg2

    @property
    def mark_answered_elsewhere_bool(self) -> bool:
        """Boolean representation of mark_answered_elsewhere."""
        return self.mark_answered_elsewhere == 1

    @mark_answered_elsewhere_bool.setter
    def mark_answered_elsewhere_bool(self, value: bool) -> None:
        """Set mark_answered_elsewhere from a boolean value."""
        self.mark_answered_elsewhere = int(value is True)

    @property
    def exten(self) -> str | None:
        """The extension number of the group."""
        for extension in self.extensions:
            return extension.exten
        return None

    @exten.expression
    def exten(cls) -> ScalarSelect[str]:
        """Retrieve the extension value for a given class instance.

        This method constructs a SQLAlchemy query to select the `exten` field from
        the `Extension` table where the `type` is "group" and the `typeval` matches
        the string representation of the class instance's `id`.

        Returns:
            Mapped[str | None]: The extension value if found, otherwise None.

        """
        return (
            select(Extension.exten)
            .where(Extension.type == "group")
            .where(Extension.typeval == cast(cls.id, String))
            .scalar_subquery()
        )
