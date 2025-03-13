# file: accent_dao/alchemy/queuefeatures.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import cast, select

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .callerid import Callerid
    from .dialaction import Dialaction
    from .extension import Extension
    from .queue import Queue
    from .queuemember import QueueMember
    from .schedulepath import SchedulePath


DEFAULT_QUEUE_OPTIONS: dict[str, str] = {
    "timeout": "15",
    "queue-youarenext": "queue-youarenext",
    "queue-thereare": "queue-thereare",
    "queue-callswaiting": "queue-callswaiting",
    "queue-holdtime": "queue-holdtime",
    "queue-minutes": "queue-minutes",
    "queue-seconds": "queue-seconds",
    "queue-thankyou": "queue-thankyou",
    "queue-reporthold": "queue-reporthold",
    "periodic-announce": "queue-periodic-announce",
    "announce-frequency": "0",
    "periodic-announce-frequency": "0",
    "announce-round-seconds": "0",
    "announce-holdtime": "no",
    "retry": "5",
    "wrapuptime": "0",
    "maxlen": "0",
    "servicelevel": "0",
    "strategy": "ringall",
    "memberdelay": "0",
    "weight": "0",
    "timeoutpriority": "conf",
    "setqueueentryvar": "1",
    "setqueuevar": "1",
}


class QueueFeatures(Base):
    """Represents features for a queue.

    Attributes:
        id: The unique identifier for the queue features.
        tenant_uuid: The UUID of the tenant the queue belongs to.
        name: The name of the queue.
        displayname: The display name of the queue.
        number: The extension number of the queue.
        context: The context associated with the queue.
        data_quality: Indicates if data quality monitoring is enabled.
        hitting_callee: Indicates if the callee can hang up with DTMF.
        hitting_caller: Indicates if the caller can hang up with DTMF.
        retries: The number of retries before fallback.
        ring: Indicates if the queue should ring on hold.
        transfer_user: Indicates if call transfer to users is allowed.
        transfer_call: Indicates if call transfer is allowed.
        write_caller: Indicates if caller information can be written.
        write_calling: Indicates if calling information can be written.
        ignore_forward: Indicates if call forwarding should be ignored.
        url: A URL associated with the queue.
        announceoverride: An announcement override.
        timeout: The timeout for the queue.
        preprocess_subroutine: A preprocess subroutine.
        announce_holdtime: Indicates if hold time should be announced.
        waittime: The wait time threshold.
        waitratio: The wait ratio.
    mark_answered_elsewhere: Flag to mark call answered by another member of this queue.
        _queue: Relationship to Queue.
        enabled: Indicates if the queue is enabled.
        options: The options for the queue.
        music_on_hold: The music on hold setting.
        caller_id: Relationship to Callerid.
        caller_id_mode: The caller ID mode.
        caller_id_name: The caller ID name.
        extensions: Relationship to Extension.
        func_keys: Relationship to FuncKeyDestQueue.
        queue_dialactions: Relationship to Dialaction, mapped by event.
        _dialaction_actions: Relationship to Dialaction.
        user_queue_members: Relationship to QueueMember for user members.
        agent_queue_members: Relationship to QueueMember for agent members.
        schedule_paths: Relationship to SchedulePath.
        schedules: Schedules for the queue.
        wait_time_destination: The destination for calls exceeding the wait time.
        wait_ratio_destination: The destination for calls exceeding the wait ratio.
        fallbacks: The fallback dialactions.
        label: The label (display name) of the queue.
        data_quality_bool: Boolean representation of data_quality.
        ignore_forward_bool: Boolean representation of ignore_forward.
        dtmf_hangup_callee_enabled: Indicates if DTMF hangup is enabled for callees.
    dtmf_hangup_caller_enabled: Indicates if DTMF hangup is enabled for callers.
    dtmf_transfer_callee_enabled: Indicates if DTMF transfer is enabled for callees.
    dtmf_transfer_caller_enabled: Indicates if DTMF transfer is enabled for callers.
    dtmf_record_callee_enabled: Indicates if DTMF recording is enabled for callees.
    dtmf_record_caller_enabled: Indicates if DTMF recording is enabled for callers.
        retry_on_timeout: Indicates if retries on timeout are enabled.
        ring_on_hold: Indicates if ringing on hold is enabled.
    announce_hold_time_on_entry: Indicates if hold time announcement on entry is enabled.
        wait_time_threshold: The wait time threshold.
        wait_ratio_threshold: The wait ratio threshold.
    mark_answered_elsewhere_bool: Boolean representation of mark_answered_elsewhere.
        exten: The extension number.

    """

    __tablename__: str = "queuefeatures"
    __table_args__: tuple = (
        Index("queuefeatures__idx__context", "context"),
        Index("queuefeatures__idx__number", "number"),
        Index("queuefeatures__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    displayname: Mapped[str] = mapped_column(String(128), nullable=False)
    number: Mapped[str | None] = mapped_column(String(40), nullable=True)
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    data_quality: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    hitting_callee: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    hitting_caller: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    retries: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    ring: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
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
    url: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    announceoverride: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default=""
    )
    timeout: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preprocess_subroutine: Mapped[str | None] = mapped_column(String(79), nullable=True)
    announce_holdtime: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    waittime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    waitratio: Mapped[float | None] = mapped_column(DOUBLE_PRECISION, nullable=True)
    mark_answered_elsewhere: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )

    _queue: Mapped["Queue"] = relationship(
        "Queue",
        primaryjoin="""and_(
            Queue.category == 'queue',
            Queue.name == QueueFeatures.name
        )""",
        foreign_keys="Queue.name",
        cascade="all, delete-orphan",
        uselist=False,
        passive_updates=False,
    )

    @property
    def enabled(self) -> bool | None:
        return self._queue.enabled if self._queue else None

    @property
    def options(self) -> list[list[str]]:
        return self._queue.options if self._queue else []

    @property
    def music_on_hold(self) -> str | None:
        return self._queue.musicclass if self._queue else None

    caller_id: Mapped["Callerid"] = relationship(
        "Callerid",
        primaryjoin="""and_(
            Callerid.type == 'queue',
            Callerid.typeval == QueueFeatures.id
        )""",
        foreign_keys="Callerid.typeval",
        cascade="all, delete-orphan",
        uselist=False,
    )

    @property
    def caller_id_mode(self) -> str | None:
        return self.caller_id.mode if self.caller_id else None

    @caller_id_mode.setter
    def caller_id_mode(self, value: str) -> None:
        if self.caller_id:
            self.caller_id.mode = value
        else:
            self.caller_id = Callerid(type="queue", mode=value)

    @property
    def caller_id_name(self) -> str | None:
        return self.caller_id.name if self.caller_id else None

    @caller_id_name.setter
    def caller_id_name(self, value: str | None) -> None:
        if self.caller_id:
            self.caller_id.name = value
        else:
            self.caller_id = Callerid(type="queue", name=value)

    extensions: Mapped[list["Extension"]] = relationship(
        "Extension",
        primaryjoin="""and_(
            Extension.type == 'queue',
            Extension.typeval == cast(QueueFeatures.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    func_keys: Mapped[list["FuncKeyDestQueue"]] = relationship(
        "FuncKeyDestQueue", cascade="all, delete-orphan"
    )

    # Removed attribute_mapped_collection
    queue_dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'queue',
            Dialaction.categoryval == cast(QueueFeatures.id, String)
        )""",
        foreign_keys="Dialaction.categoryval",
        cascade="all, delete-orphan",
    )

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'queue',
            Dialaction.actionarg1 == cast(QueueFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    user_queue_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'queue',
            QueueMember.usertype == 'user',
            QueueMember.queue_name == QueueFeatures.name
        )""",
        foreign_keys="QueueMember.queue_name",
        order_by="QueueMember.position",
        cascade="all, delete-orphan",
    )

    agent_queue_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'queue',
            QueueMember.usertype == 'agent',
            QueueMember.queue_name == QueueFeatures.name
        )""",
        foreign_keys="QueueMember.queue_name",
        order_by="QueueMember.position",
        cascade="all, delete-orphan",
    )

    schedule_paths: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.path == 'queue',
            SchedulePath.pathid == QueueFeatures.id
        )""",
        foreign_keys="SchedulePath.pathid",
        cascade="all, delete-orphan",
    )

    @property
    def schedules(self) -> list["SchedulePath"]:
        return [sp.schedule for sp in self.schedule_paths]

    @schedules.setter
    def schedules(self, value: list["SchedulePath"]) -> None:
        self.schedule_paths = [
            SchedulePath(path="queue", schedule=_schedule) for _schedule in value
        ]

    def __init__(self, options: list[list[str]] | None = None, **kwargs: Any) -> None:  # type: ignore
        """Initializes the QueueFeatures object, creating a Queue if one doesn't exist."""
        options = options or []
        options = self.merge_options_with_default_values(options)
        enabled = kwargs.pop("enabled", True)
        music_on_hold = kwargs.pop("music_on_hold", None)
        super().__init__(**kwargs)
        if not self._queue:
            self._queue = Queue(
                # 'name' is set by the relationship foreign_key
                category="queue",
                enabled=int(enabled),  # Convert to integer
                musicclass=music_on_hold,
                options=options,
            )

    def merge_options_with_default_values(
        self, options: list[list[str]]
    ) -> list[list[str]]:
        """Merges provided options with default values."""
        result: dict = dict(DEFAULT_QUEUE_OPTIONS)
        for option in options:
            result[option[0]] = option[1]
        return [[key, value] for key, value in result.items()]

    @property
    def wait_time_destination(self) -> "Dialaction" | None:
        """The destination for calls exceeding the wait time."""
        return self.queue_dialactions.get("qwaittime")

    @wait_time_destination.setter
    def wait_time_destination(self, destination: "Dialaction" | None) -> None:
        """Set the destination for calls exceeding the wait time."""
        self._set_dialaction("qwaittime", destination)

    @property
    def wait_ratio_destination(self) -> "Dialaction" | None:
        """The destination for calls exceeding the wait ratio."""
        return self.queue_dialactions.get("qwaitratio")

    @wait_ratio_destination.setter
    def wait_ratio_destination(self, destination: "Dialaction" | None) -> None:
        """Set the destination for calls exceeding the wait ratio."""
        self._set_dialaction("qwaitratio", destination)

    @property
    def fallbacks(self) -> dict[str, "Dialaction"]:
        """The fallback dialactions for the queue."""
        return self.queue_dialactions

    @fallbacks.setter
    def fallbacks(self, dialactions: dict[str, "Dialaction"]) -> None:
        """Set the fallback dialactions."""
        for event in ("noanswer", "busy", "congestion", "chanunavail"):
            if event not in dialactions:
                self.queue_dialactions.pop(event, None)  # Use pop with default

        for event, dialaction in dialactions.items():
            self._set_dialaction(event, dialaction)

    def _set_dialaction(self, event: str, dialaction: "Dialaction" | None) -> None:
        """Helper method to set a dialaction for a specific event."""
        if dialaction is None:
            self.queue_dialactions.pop(event, None)  # Use pop with default
            return

        if event not in self.queue_dialactions:
            dialaction.event = event
            dialaction.category = "queue"
            self.queue_dialactions[event] = dialaction
        else:
            self.queue_dialactions[event].action = dialaction.action
            self.queue_dialactions[event].actionarg1 = dialaction.actionarg1
            self.queue_dialactions[event].actionarg2 = dialaction.actionarg2

    def fix_extension(self) -> None:
        """Fixes the extension number and context based on associated extensions."""
        self.number = None
        self.context = None
        for extension in self.extensions:
            self.number = extension.exten
            self.context = extension.context
            return

    @property
    def label(self) -> str | None:
        """The label (display name) of the queue."""
        if self.displayname == "":
            return None
        return self.displayname

    @label.setter
    def label(self, value: str | None) -> None:
        """Set the label (display name) of the queue."""
        if value is None:
            self.displayname = ""
        else:
            self.displayname = value

    @label.expression
    def label(cls) -> Mapped[str | None]:
        return func.nullif(cls.displayname, "")

    @property
    def data_quality_bool(self) -> bool:
        """Boolean representation of data_quality."""
        return self.data_quality == 1

    @data_quality_bool.setter
    def data_quality_bool(self, value: bool) -> None:
        """Set the data_quality setting."""
        self.data_quality = int(value is True)

    @property
    def ignore_forward_bool(self) -> bool:
        """Boolean representation of ignore_forward."""
        return self.ignore_forward == 1

    @ignore_forward_bool.setter
    def ignore_forward_bool(self, value: bool) -> None:
        """Set the ignore_forward setting."""
        self.ignore_forward = int(value is True)

    @property
    def dtmf_hangup_callee_enabled(self) -> bool:
        """Indicates if DTMF hangup is enabled for callees."""
        return self.hitting_callee == 1

    @dtmf_hangup_callee_enabled.setter
    def dtmf_hangup_callee_enabled(self, value: bool) -> None:
        """Set whether DTMF hangup is enabled for callees."""
        self.hitting_callee = int(value is True)

    @property
    def dtmf_hangup_caller_enabled(self) -> bool:
        """Indicates if DTMF hangup is enabled for callers."""
        return self.hitting_caller == 1

    @dtmf_hangup_caller_enabled.setter
    def dtmf_hangup_caller_enabled(self, value: bool) -> None:
        """Set whether DTMF hangup is enabled for callers."""
        self.hitting_caller = int(value is True)

    @property
    def dtmf_transfer_callee_enabled(self) -> bool:
        """Indicates if DTMF transfer is enabled for callees."""
        return self.transfer_user == 1

    @dtmf_transfer_callee_enabled.setter
    def dtmf_transfer_callee_enabled(self, value: bool) -> None:
        """Set whether DTMF transfer is enabled for callees."""
        self.transfer_user = int(value is True)

    @property
    def dtmf_transfer_caller_enabled(self) -> bool:
        """Indicates if DTMF transfer is enabled for callers."""
        return self.transfer_call == 1

    @dtmf_transfer_caller_enabled.setter
    def dtmf_transfer_caller_enabled(self, value: bool) -> None:
        """Set whether DTMF transfer is enabled for callers."""
        self.transfer_call = int(value is True)

    @property
    def dtmf_record_callee_enabled(self) -> bool:
        """Indicates if DTMF recording is enabled for callees."""
        return self.write_caller == 1

    @dtmf_record_callee_enabled.setter
    def dtmf_record_callee_enabled(self, value: bool) -> None:
        """Set whether DTMF recording is enabled for callees."""
        self.write_caller = int(value is True)

    @property
    def dtmf_record_caller_enabled(self) -> bool:
        """Indicates if DTMF recording is enabled for callers."""
        return self.write_calling == 1

    @dtmf_record_caller_enabled.setter
    def dtmf_record_caller_enabled(self, value: bool) -> None:
        """Set whether DTMF recording is enabled for callers."""
        self.write_calling = int(value is True)

    @property
    def retry_on_timeout(self) -> bool:
        """Indicates if retries on timeout are enabled."""
        return not self.retries == 1

    @retry_on_timeout.setter
    def retry_on_timeout(self, value: bool) -> None:
        """Set whether retries on timeout are enabled."""
        self.retries = int(value is False)

    @property
    def ring_on_hold(self) -> bool:
        """Indicates if ringing on hold is enabled."""
        return self.ring == 1

    @ring_on_hold.setter
    def ring_on_hold(self, value: bool) -> None:
        """Set the ringing on hold setting."""
        self.ring = int(value is True)

    @property
    def announce_hold_time_on_entry(self) -> bool:
        """Indicates if hold time announcement on entry is enabled."""
        return self.announce_holdtime == 1

    @announce_hold_time_on_entry.setter
    def announce_hold_time_on_entry(self, value: bool) -> None:
        """Set the hold time announcement on entry setting."""
        self.announce_holdtime = int(value is True)

    @property
    def wait_time_threshold(self) -> int | None:
        """The wait time threshold."""
        return self.waittime

    @wait_time_threshold.setter
    def wait_time_threshold(self, value: int | None) -> None:
        """Set the wait time threshold."""
        self.waittime = value

    @property
    def wait_ratio_threshold(self) -> float | None:
        """The wait ratio threshold."""
        return self.waitratio

    @wait_ratio_threshold.setter
    def wait_ratio_threshold(self, value: float | None) -> None:
        """Set the wait ratio threshold."""
        self.waitratio = value

    @property
    def mark_answered_elsewhere_bool(self) -> bool:
        return self.mark_answered_elsewhere == 1

    @mark_answered_elsewhere_bool.setter
    def mark_answered_elsewhere_bool(self, value: bool) -> None:
        self.mark_answered_elsewhere = int(value is True)

    @property
    def exten(self) -> str | None:
        """The extension number of the queue."""
        for extension in self.extensions:
            return extension.exten
        return None

    @exten.expression
    def exten(cls) -> Mapped[str | None]:
        return (
            select(Extension.exten)
            .where(Extension.type == "queue")
            .where(Extension.typeval == cast(cls.id, String))
            .scalar_subquery()
        )
