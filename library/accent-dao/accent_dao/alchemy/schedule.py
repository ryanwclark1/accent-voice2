# file: accent_dao/alchemy/schedule.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import cast, func

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .application import Application
    from .conference import Conference
    from .groupfeatures import GroupFeatures
    from .ivr import IVR
    from .queuefeatures import QueueFeatures
    from .schedule_time import ScheduleTime
    from .schedulepath import SchedulePath
    from .switchboard import Switchboard
    from .userfeatures import UserFeatures
    from .voicemail import Voicemail

DialactionAction = Literal[
    "none",
    "endcall:busy",
    "endcall:congestion",
    "endcall:hangup",
    "user",
    "group",
    "queue",
    "voicemail",
    "extension",
    "outcall",
    "application:callbackdisa",
    "application:disa",
    "application:directory",
    "application:faxtomail",
    "application:voicemailmain",
    "application:password",
    "sound",
    "custom",
    "ivr",
    "conference",
    "switchboard",
    "application:custom",
]


class Schedule(Base):
    """Represents a schedule.

    Attributes:
        id: The unique identifier for the schedule.
        tenant_uuid: The UUID of the tenant the schedule belongs to.
        name: The name of the schedule.
        timezone: The timezone for the schedule.
        fallback_action: The fallback action to take if no time periods match.
        fallback_actionid: The ID of the entity for the fallback action.
        fallback_actionargs: Additional arguments for the fallback action.
        description: A description of the schedule.
        commented: Indicates if the schedule is commented out.
        periods: Relationship to ScheduleTime.
        schedule_paths: Relationship to SchedulePath.
        schedule_incalls: Relationship to SchedulePath for incall paths.
        incalls: Inbound call routes associated with the schedule.
        schedule_users: Relationship to SchedulePath for user paths.
        users: Users associated with the schedule.
        schedule_groups: Relationship to SchedulePath for group paths.
        groups: Groups associated with the schedule.
        schedule_outcalls: Relationship to SchedulePath for outcall paths.
        outcalls: Outbound call routes associated with the schedule.
        schedule_queues: Relationship to SchedulePath for queue paths.
        queues: Queues associated with the schedule.
        conference: Relationship to Conference (for fallback action).
        group: Relationship to GroupFeatures (for fallback action).
        user: Relationship to UserFeatures (for fallback action).
        ivr: Relationship to IVR (for fallback action).
        switchboard: Relationship to Switchboard (for fallback action).
        voicemail: Relationship to Voicemail (for fallback action).
        application: Relationship to Application (for fallback action).
        queue: Relationship to QueueFeatures (for fallback action).
        open_periods: Time periods when the schedule is open.
        exceptional_periods: Time periods when the schedule is closed (exceptions).
        closed_destination: The destination for calls when the schedule is closed.
        type: The type of the fallback action.
        subtype: The subtype of the fallback action.
        actionarg1: The first argument for the fallback action.
        actionarg2: The second argument for the fallback action.
        enabled: Indicates if the schedule is enabled.

    """

    __tablename__: str = "schedule"
    __table_args__: tuple = (Index("schedule__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(128), nullable=True)
    fallback_action: Mapped[DialactionAction] = mapped_column(
        String,
        nullable=False,
        server_default="none",
    )
    fallback_actionid: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fallback_actionargs: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    periods: Mapped[list["ScheduleTime"]] = relationship(
        "ScheduleTime",
        primaryjoin="ScheduleTime.schedule_id == Schedule.id",
        foreign_keys="ScheduleTime.schedule_id",
        cascade="all, delete-orphan",
    )

    schedule_paths: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath", cascade="all, delete-orphan"
    )

    schedule_incalls: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.schedule_id == Schedule.id,
            SchedulePath.path == 'incall'
        )""",
        viewonly=True,
    )

    @property
    def incalls(self) -> list["SchedulePath"]:
        return [si.incall for si in self.schedule_incalls if si.incall]

    schedule_users: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.schedule_id == Schedule.id,
            SchedulePath.path == 'user'
        )""",
        viewonly=True,
    )

    @property
    def users(self) -> list["SchedulePath"]:
        return [su.user for su in self.schedule_users if su.user]

    schedule_groups: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.schedule_id == Schedule.id,
            SchedulePath.path == 'group'
        )""",
        viewonly=True,
    )

    @property
    def groups(self) -> list["SchedulePath"]:
        return [sg.group for sg in self.schedule_groups if sg.group]

    schedule_outcalls: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.schedule_id == Schedule.id,
            SchedulePath.path == 'outcall'
        )""",
        viewonly=True,
    )

    @property
    def outcalls(self) -> list["SchedulePath"]:
        return [so.outcall for so in self.schedule_outcalls if so.outcall]

    schedule_queues: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.schedule_id == Schedule.id,
            SchedulePath.path == 'queue'
        )""",
        viewonly=True,
    )

    @property
    def queues(self) -> list["SchedulePath"]:
        return [sq.queue for sq in self.schedule_queues if sq.queue]

    # Begin definitions for fallback destination
    conference: Mapped["Conference"] = relationship(
        "Conference",
        primaryjoin="""and_(
            Schedule.fallback_action == 'conference',
            Schedule.fallback_actionid == cast(Conference.id, String)
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            Schedule.fallback_action == 'group',
            Schedule.fallback_actionid == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            Schedule.fallback_action == 'user',
            Schedule.fallback_actionid == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )

    ivr: Mapped["IVR"] = relationship(
        "IVR",
        primaryjoin="""and_(
            Schedule.fallback_action == 'ivr',
            Schedule.fallback_actionid == cast(IVR.id, String)
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )

    switchboard: Mapped["Switchboard"] = relationship(
        "Switchboard",
        primaryjoin="""and_(
            Schedule.fallback_action == 'switchboard',
            Schedule.fallback_actionid == Switchboard.uuid
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )

    voicemail: Mapped["Voicemail"] = relationship(
        "Voicemail",
        primaryjoin="""and_(
            Schedule.fallback_action == 'voicemail',
            Schedule.fallback_actionid == cast(Voicemail.id, String)
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )

    application: Mapped["Application"] = relationship(
        "Application",
        primaryjoin="""and_(
            Schedule.fallback_action == 'application:custom',
            Schedule.fallback_actionid == Application.uuid
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )

    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="""and_(
            Schedule.fallback_action == 'queue',
            Schedule.fallback_actionid == cast(QueueFeatures.id, String)
        )""",
        foreign_keys="Schedule.fallback_actionid",
        viewonly=True,
    )
    # End definitions for fallback destination

    @property
    def open_periods(self) -> list["ScheduleTime"]:
        """Time periods when the schedule is open."""
        return self._get_periods("opened")

    @open_periods.setter
    def open_periods(self, value: list["ScheduleTime"]) -> None:
        """Set the open time periods."""
        self._set_periods("opened", value)

    @property
    def exceptional_periods(self) -> list["ScheduleTime"]:
        """Time periods when the schedule is closed (exceptions)."""
        return self._get_periods("closed")

    @exceptional_periods.setter
    def exceptional_periods(self, value: list["ScheduleTime"]) -> None:
        """Set the exceptional (closed) time periods."""
        self._set_periods("closed", value)

    def _get_periods(self, mode: str) -> list["ScheduleTime"]:
        """Helper method to get periods by mode."""
        return [period for period in self.periods if period.mode == mode]

    def _set_periods(self, mode: str, periods: list["ScheduleTime"]) -> None:
        """Helper method to set periods by mode."""
        self.periods = [period for period in self.periods if period.mode != mode]
        for period in periods:
            period.mode = mode
            self.periods.append(period)

    @property
    def closed_destination(self) -> "Schedule":
        """The destination for calls when the schedule is closed."""
        return self

    @property
    def type(self) -> str:
        """The type of the fallback action."""
        return self.fallback_action.split(":")[0]

    @type.setter
    def type(self, value: str) -> None:
        """Set the type of the fallback action."""
        self.fallback_action = (
            f"{value}:{self.subtype}" if self.subtype else value  # type: ignore
        )

    @property
    def subtype(self) -> str | None:
        """The subtype of the fallback action."""
        if ":" not in self.fallback_action:
            return None
        return self.fallback_action.split(":")[1]

    @subtype.setter
    def subtype(self, value: str | None) -> None:
        """Set the subtype of the fallback action."""
        if value is None:
            self.fallback_action = self.type  # type: ignore
        else:
            self.fallback_action = f"{self.type}:{value}"  # type: ignore

    @property
    def actionarg1(self) -> str | None:
        """The first argument for the fallback action."""
        if self.fallback_actionid == "":
            return None
        return self.fallback_actionid

    @actionarg1.setter
    def actionarg1(self, value: str | None) -> None:
        """Set the first argument for the fallback action."""
        self.fallback_actionid = value

    @property
    def actionarg2(self) -> str | None:
        """The second argument for the fallback action."""
        if self.fallback_actionargs == "":
            return None
        return self.fallback_actionargs

    @actionarg2.setter
    def actionarg2(self, value: str | None) -> None:
        """Set the second argument for the fallback action."""
        self.fallback_actionargs = value

    @property
    def enabled(self) -> bool:
        """Indicates if the schedule is enabled."""
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disables the schedule."""
        self.commented = int(not value)

    @enabled.expression
    def enabled(cls) -> Mapped[bool]:
        return func.not_(cast(cls.commented, Boolean))
