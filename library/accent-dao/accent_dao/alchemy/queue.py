# file: accent_dao/alchemy/queue.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.asterisk import AsteriskOptionsMixin
from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .groupfeatures import GroupFeatures
    from .queuefeatures import QueueFeatures

QueueCategory = Literal["group", "queue"]
QueueMonitorType = Literal["no", "mixmonitor"]
QueueStrategy = Literal[
    "ringall",
    "roundrobin",
    "leastrecent",
    "fewestcalls",
    "random",
    "rrmemory",
]  # Added Strategy
QueueAutopause = Literal["no", "yes", "all"]


class Queue(Base, AsteriskOptionsMixin):
    """Represents a queue.

    Implements AsteriskOptionsMixin for managing Asterisk options.

    Attributes:
    ... (All the queue attributes)
    groupfeatures: Relationship to GroupFeatures (if category is 'group').
    queuefeatures: Relationship to QueueFeatures (if category is 'queue').
    enabled: Indicates if the queue is enabled.
    ring_in_use: Indicates if the ring-in-use setting is enabled.
    label: The display name or label of the queue.

    Inherited from AsteriskOptionsMixin:
        options: A list of key-value pairs representing Asterisk options.

    """

    EXCLUDE_OPTIONS: set[str] = {  # noqa: RUF012
        "name",
        "category",
        "commented",
    }
    EXCLUDE_OPTIONS_CONFD: set[str] = {  # noqa: RUF012
        "musicclass",
    }
    AST_TRUE_INTEGER_COLUMNS: set[str] = {  # noqa: RUF012
        "ringinuse",
        "timeoutrestart",
        "autofill",
        "setinterfacevar",
        "setqueueentryvar",
        "setqueuevar",
        "reportholdtime",
        "random-periodic-announce",
    }

    __tablename__: str = "queue"

    name: Mapped[str] = mapped_column(String(128), primary_key=True)
    musicclass: Mapped[str | None] = mapped_column(String(128), nullable=True)
    announce: Mapped[str | None] = mapped_column(String(128), nullable=True)
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    timeout: Mapped[int | None] = mapped_column(
        Integer, server_default="0", nullable=True
    )
    monitor_type: Mapped[QueueMonitorType | None] = mapped_column(
        "monitor-type",
        Enum("no", "mixmonitor", name="queue_monitor_type"),
        nullable=True,
    )
    monitor_format: Mapped[str | None] = mapped_column(
        "monitor-format", String(128), nullable=True
    )
    queue_youarenext: Mapped[str | None] = mapped_column(
        "queue-youarenext", String(128), nullable=True
    )
    queue_thereare: Mapped[str | None] = mapped_column(
        "queue-thereare", String(128), nullable=True
    )
    queue_callswaiting: Mapped[str | None] = mapped_column(
        "queue-callswaiting", String(128), nullable=True
    )
    queue_holdtime: Mapped[str | None] = mapped_column(
        "queue-holdtime", String(128), nullable=True
    )
    queue_minutes: Mapped[str | None] = mapped_column(
        "queue-minutes", String(128), nullable=True
    )
    queue_seconds: Mapped[str | None] = mapped_column(
        "queue-seconds", String(128), nullable=True
    )
    queue_thankyou: Mapped[str | None] = mapped_column(
        "queue-thankyou", String(128), nullable=True
    )
    queue_reporthold: Mapped[str | None] = mapped_column(
        "queue-reporthold", String(128), nullable=True
    )
    periodic_announce: Mapped[str | None] = mapped_column(Text, nullable=True)
    announce_frequency: Mapped[int | None] = mapped_column(
        "announce-frequency", Integer, nullable=True
    )
    periodic_announce_frequency: Mapped[int | None] = mapped_column(
        "periodic-announce-frequency", Integer, nullable=True
    )
    announce_round_seconds: Mapped[int | None] = mapped_column(
        "announce-round-seconds", Integer, nullable=True
    )
    announce_holdtime: Mapped[str | None] = mapped_column(
        "announce-holdtime", String(4), nullable=True
    )
    retry: Mapped[int | None] = mapped_column(Integer, nullable=True)
    wrapuptime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    maxlen: Mapped[int | None] = mapped_column(Integer, nullable=True)
    servicelevel: Mapped[int | None] = mapped_column(Integer, nullable=True)
    strategy: Mapped[str | None] = mapped_column(String(11), nullable=True)
    joinempty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    leavewhenempty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ringinuse: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    reportholdtime: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    memberdelay: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timeoutrestart: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    category: Mapped[QueueCategory] = mapped_column(
        Enum("group", "queue", name="queue_category"),
        nullable=False,
    )
    timeoutpriority: Mapped[str] = mapped_column(
        String(10), nullable=False, server_default="app"
    )
    autofill: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )  # Integer representation
    autopause: Mapped[QueueAutopause] = mapped_column(
        String(3), nullable=False, server_default="no"
    )
    setinterfacevar: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    setqueueentryvar: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    setqueuevar: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    membermacro: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    min_announce_frequency: Mapped[int] = mapped_column(
        "min-announce-frequency", Integer, nullable=False, server_default="60"
    )
    random_periodic_announce: Mapped[int] = mapped_column(
        "random-periodic-announce", Integer, nullable=False, server_default="0"
    )
    announce_position: Mapped[str] = mapped_column(
        "announce-position", String(1024), nullable=False, server_default="yes"
    )
    announce_position_limit: Mapped[int] = mapped_column(
        "announce-position-limit", Integer, nullable=False, server_default="5"
    )
    defaultrule: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    groupfeatures: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            Queue.category == 'group',
            Queue.name == GroupFeatures.name
        )""",
        foreign_keys="Queue.name",
        uselist=False,
    )

    queuefeatures: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="""and_(
            Queue.category == 'queue',
            Queue.name == QueueFeatures.name
        )""",
        foreign_keys="Queue.name",
        uselist=False,
    )

    @property
    def enabled(self) -> bool | None:
        """Indicates if the queue is enabled."""
        if self.commented is None:
            return None
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        """Enable or disables the queue."""
        self.commented = int(not value) if value is not None else None

    @property
    def ring_in_use(self) -> bool:
        """Indicates if the ring-in-use setting is enabled."""
        return bool(self.ringinuse)

    @ring_in_use.setter
    def ring_in_use(self, value: bool) -> None:
        """Set the ring-in-use setting."""
        self.ringinuse = int(value)  # Convert to integer

    @property
    def label(self) -> str:
        """The display name or label of the queue."""
        try:
            if self.category == "group":
                return self.groupfeatures.label  # type: ignore
            if self.category == "queue":
                return self.queuefeatures.displayname  # type: ignore
        except AttributeError:
            pass
        return "unknown"
