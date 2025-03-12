# file: accent_dao/models/schedule_time.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .application import Application
    from .conference import Conference
    from .groupfeatures import GroupFeatures
    from .ivr import IVR
    from .queuefeatures import QueueFeatures
    from .switchboard import Switchboard
    from .userfeatures import UserFeatures
    from .voicemail import Voicemail

ScheduleTimeMode = Literal["opened", "closed"]
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


class ScheduleTime(Base):
    """Represents a time period within a schedule.

    Attributes:
        id: The unique identifier for the schedule time.
        schedule_id: The ID of the associated schedule.
        mode: The mode of the time period ('opened' or 'closed').
        hours: The hours defined for the time period (e.g., '9-17').
        weekdays: The weekdays for the time period (e.g., '1-5' for Monday-Friday).
        monthdays: The days of the month for the time period.
        months: The months for the time period.
        action: The action to perform during this time period.
        actionid: The ID of the entity for the action.
        actionargs: Additional arguments for the action.
        commented: Indicates if the time period is commented out.
        conference: Relationship to Conference (for action).
        group: Relationship to GroupFeatures (for action).
        user: Relationship to UserFeatures (for action).
        ivr: Relationship to IVR (for action).
        switchboard: Relationship to Switchboard (for action).
        voicemail: Relationship to Voicemail (for action).
        application: Relationship to Application (for action).
        queue: Relationship to QueueFeatures (for action).
        destination: The destination for the time period.
        hours_start: The starting hour.
        hours_end: The ending hour.
        week_days: A list of integers representing the weekdays.
        month_days: A list of integers representing the days of the month.
        months_list: A list of integers representing the months.
        type: The type of the action.
        subtype: The subtype of the action.
        actionarg1: The first argument for the action.
        actionarg2: The second argument for the action.

    """

    __tablename__: str = "schedule_time"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schedule_id: Mapped[int] = mapped_column(Integer)
    mode: Mapped[ScheduleTimeMode] = mapped_column(
        Enum("opened", "closed", name="schedule_time_mode"),
        nullable=False,
        server_default="opened",
    )
    hours: Mapped[str | None] = mapped_column(String(512), nullable=True)
    weekdays: Mapped[str | None] = mapped_column(String(512), nullable=True)
    monthdays: Mapped[str | None] = mapped_column(String(512), nullable=True)
    months: Mapped[str | None] = mapped_column(String(512), nullable=True)
    action: Mapped[DialactionAction] = mapped_column(String, nullable=False)
    actionid: Mapped[str | None] = mapped_column(String(255), nullable=True)
    actionargs: Mapped[str | None] = mapped_column(String(255), nullable=True)
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    conference: Mapped["Conference"] = relationship(
        "Conference",
        primaryjoin="""and_(
            ScheduleTime.action == 'conference',
            ScheduleTime.actionid == cast(Conference.id, String)
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            ScheduleTime.action == 'group',
            ScheduleTime.actionid == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            ScheduleTime.action == 'user',
            ScheduleTime.actionid == cast(UserFeatures.id, String)
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    ivr: Mapped["IVR"] = relationship(
        "IVR",
        primaryjoin="""and_(
            ScheduleTime.action == 'ivr',
            ScheduleTime.actionid == cast(IVR.id, String)
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    switchboard: Mapped["Switchboard"] = relationship(
        "Switchboard",
        primaryjoin="""and_(
            ScheduleTime.action == 'switchboard',
            ScheduleTime.actionid == Switchboard.uuid
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    voicemail: Mapped["Voicemail"] = relationship(
        "Voicemail",
        primaryjoin="""and_(
            ScheduleTime.action == 'voicemail',
            ScheduleTime.actionid == cast(Voicemail.id, String)
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    application: Mapped["Application"] = relationship(
        "Application",
        primaryjoin="""and_(
            ScheduleTime.action == 'application:custom',
            ScheduleTime.actionid == Application.uuid
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="""and_(
            ScheduleTime.action == 'queue',
            ScheduleTime.actionid == cast(QueueFeatures.id, String)
        )""",
        foreign_keys="ScheduleTime.actionid",
        viewonly=True,
    )

    @property
    def destination(self) -> "ScheduleTime":
        """The destination for the time period."""
        return self

    @property
    def hours_start(self) -> str | None:
        """The starting hour."""
        return self.hours.split("-", 1)[0] if self.hours else None

    @hours_start.setter
    def hours_start(self, value: str | None) -> None:
        """Set the starting hour."""
        hours_start = value if value else ""
        hours_end = self.hours_end if self.hours_end else ""
        self._set_hours(hours_start, hours_end)

    @property
    def hours_end(self) -> str | None:
        """The ending hour."""
        hours = self.hours.split("-", 1) if self.hours else ""
        return hours[1] if len(hours) == 2 else None

    @hours_end.setter
    def hours_end(self, value: str | None) -> None:
        """Set the ending hour."""
        hours_start = self.hours_start if self.hours_start else ""
        hours_end = value if value else ""
        self._set_hours(hours_start, hours_end)

    def _set_hours(self, hours_start: str, hours_end: str) -> None:
        """Helper method to set the hours string."""
        end_suffix = f"-{hours_end}" if hours_end else ""
        self.hours = f"{hours_start}{end_suffix}"

    @property
    def week_days(self) -> list[int]:
        """A list of integers representing the weekdays."""
        if not self.weekdays:
            return list(range(1, 8))  # Default: all weekdays
        return self._expand_range(self.weekdays)

    @week_days.setter
    def week_days(self, value: list[int] | None) -> None:
        """Set the weekdays."""
        self.weekdays = self._convert_array_to_str(value)

    @property
    def month_days(self) -> list[int]:
        """A list of integers representing the days of the month."""
        if not self.monthdays:
            return list(range(1, 32))  # Default: all days of the month
        return self._expand_range(self.monthdays)

    @month_days.setter
    def month_days(self, value: list[int] | None) -> None:
        """Set the days of the month."""
        self.monthdays = self._convert_array_to_str(value)

    @property
    def months_list(self) -> list[int]:
        """A list of integers representing the months."""
        if not self.months:
            return list(range(1, 13))  # Default: all months
        return self._expand_range(self.months)

    @months_list.setter
    def months_list(self, value: list[int] | None) -> None:
        """Set the months."""
        self.months = self._convert_array_to_str(value)

    def _expand_range(self, multi_range: str) -> list[int]:
        """Expands a string representation of ranges into a list of integers.

        Args:
            multi_range: A string like "1-5,7,9-12".

        Returns:
            A list of integers representing the expanded range.

        """
        if not multi_range:
            return []

        result = []
        for item in multi_range.split(","):
            if "-" in item:
                start, end = map(int, item.split("-", 2))
                result += list(range(start, end + 1))
            else:
                result.append(int(item))
        return result

    def _convert_array_to_str(self, value: list[int] | None) -> str | None:
        """Converts a list of integers to a comma-separated string representation.

        Args:
            value: The list of integers.

        Returns:
            A comma-separated string, or None if the input is None.

        """
        return ",".join(str(x) for x in value) if value else None

    @property
    def type(self) -> str:
        """The type of the action."""
        return self.action.split(":")[0]

    @type.setter
    def type(self, value: str) -> None:
        """Set the type of the action."""
        self.action = f"{value}:{self.subtype}" if self.subtype else value  # type: ignore

    @property
    def subtype(self) -> str | None:
        """The subtype of the action."""
        if ":" not in self.action:
            return None
        return self.action.split(":")[1]

    @subtype.setter
    def subtype(self, value: str | None) -> None:
        """Set the subtype of the action."""
        if value is not None:
            self.action = f"{self.type}:{value}"  # type: ignore
        else:
            self.action = self.type  # type: ignore

    @property
    def actionarg1(self) -> str | None:
        """The first argument for the action."""
        return self.actionid

    @actionarg1.setter
    def actionarg1(self, value: str | None) -> None:
        """Set the first argument for the action."""
        self.actionid = value

    @property
    def actionarg2(self) -> str | None:
        """The second argument for the action."""
        return self.actionargs

    @actionarg2.setter
    def actionarg2(self, value: str | None) -> None:
        """Set the second argument for the action."""
        self.actionargs = value
