# file: accent_dao/alchemy/outcall.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from accent_dao.helpers.db_manager import Base

from .dialpattern import DialPattern
from .outcalltrunk import OutcallTrunk
from .rightcallmember import RightCallMember
from .schedulepath import SchedulePath

if TYPE_CHECKING:
    from .dialaction import Dialaction


class Outcall(Base):
    """Represents an outbound call route.

    Attributes:
        id: The unique identifier for the outbound call route.
        tenant_uuid: The UUID of the tenant the route belongs to.
        name: The name of the route.
        context: The context associated with the route.
        internal: Indicates if the route is for internal calls only.
        preprocess_subroutine: A preprocess subroutine.
        hangupringtime: The ring time before hanging up.
        commented: Indicates if the route is commented out.
        description: A description of the route.
        dialpatterns: Relationship to DialPattern.
        extensions: The extensions associated with the outcall.
        outcall_trunks: Relationship to OutcallTrunk.
        trunks: The trunks for this outcall.
        _dialaction_actions: Relationship to Dialaction.
        schedule_paths: Relationship to SchedulePath.
        schedules: Schedules for outcall.
        rightcall_members: Relationship to RightCallMember.
        call_permissions: Call permissions for the outcall route.
        internal_caller_id: Indicates if internal caller ID should be used.
        ring_time: The ring time.
        enabled: Indicates if the route is enabled.

    """

    __tablename__: str = "outcall"
    __table_args__: tuple = (Index("outcall__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    internal: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    preprocess_subroutine: Mapped[str | None] = mapped_column(String(79), nullable=True)
    hangupringtime: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    dialpatterns: Mapped[list["DialPattern"]] = relationship(
        "DialPattern",
        primaryjoin="""and_(
            DialPattern.type == 'outcall',
            DialPattern.typeid == Outcall.id
        )""",
        foreign_keys="DialPattern.typeid",
        cascade="all, delete-orphan",
    )

    @property
    def extensions(self) -> list["DialPattern"]:
        return [d.extension for d in self.dialpatterns]

    outcall_trunks: Mapped[list["OutcallTrunk"]] = relationship(
        "OutcallTrunk",
        order_by="OutcallTrunk.priority",
        # collection_class=ordering_list("priority"), # Removed ordering list
        cascade="all, delete-orphan",
        back_populates="outcall",
    )

    @property
    def trunks(self) -> list["OutcallTrunk"]:
        return [ot.trunk for ot in self.outcall_trunks]

    @trunks.setter
    def trunks(self, value: list["OutcallTrunk"]) -> None:
        self.outcall_trunks = [OutcallTrunk(trunk=v) for v in value]

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'outcall',
            Dialaction.actionarg1 == cast(Outcall.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    schedule_paths: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.path == 'outcall',
            SchedulePath.pathid == Outcall.id
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
            SchedulePath(
                path="outcall",
                schedule_id=_schedule.id,
                schedule=_schedule,
            )
            for _schedule in value
        ]

    rightcall_members: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="""and_(
            RightCallMember.type == 'outcall',
            RightCallMember.typeval == cast(Outcall.id, String)
        )""",
        foreign_keys="RightCallMember.typeval",
        cascade="all, delete-orphan",
    )

    @property
    def call_permissions(self):
        return [m.rightcall for m in self.rightcall_members if m.rightcall]

    @call_permissions.setter
    def call_permissions(self, value: list["RightCall"]) -> None:
        self.rightcall_members = [
            RightCallMember(
                type="outcall",
                typeval=str(permission.id),
                rightcall=permission,
            )
            for permission in value
        ]

    @property
    def internal_caller_id(self) -> bool:
        """Indicates if internal caller ID should be used."""
        return self.internal == 1

    @internal_caller_id.setter
    def internal_caller_id(self, value: bool) -> None:
        """Set whether to use internal caller ID."""
        self.internal = int(value == 1)

    @internal_caller_id.expression
    def internal_caller_id(cls) -> Mapped[bool]:
        return func.cast(cls.internal, Boolean)

    @property
    def ring_time(self) -> int | None:
        """The ring time (in seconds)."""
        if self.hangupringtime == 0:
            return None
        return self.hangupringtime

    @ring_time.setter
    def ring_time(self, value: int | None) -> None:
        """Set the ring time."""
        if value is None:
            self.hangupringtime = 0
        else:
            self.hangupringtime = value

    @property
    def enabled(self) -> bool:
        """Indicates if the route is enabled."""
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disables the route."""
        self.commented = int(not value)

    @enabled.expression
    def enabled(cls) -> Mapped[bool]:
        return func.not_(cast(cls.commented, Boolean))

    def associate_extension(self, extension: "Extension", **kwargs: Any) -> None:
        """Associates an extension with the outcall route."""
        if extension not in self.extensions:
            extension.type = "outcall"
            dialpattern = DialPattern(type="outcall", exten=extension.exten, **kwargs)
            self.dialpatterns.append(dialpattern)
            index = self.dialpatterns.index(dialpattern)
            self.dialpatterns[index].extension = extension
            self._fix_context()

    def dissociate_extension(self, extension: "Extension") -> None:
        """Dissociates an extension from the outcall route."""
        if extension in self.extensions:
            self.extensions.remove(extension)
            extension.type = "user"
            extension.typeval = "0"
            self._fix_context()

    def update_extension_association(
        self, extension: "Extension", **kwargs: Any
    ) -> None:
        """Update the association between the outcall route and an extension."""
        for dialpattern in self.dialpatterns:
            if extension == dialpattern.extension:
                dialpattern.strip_digits = kwargs.get(
                    "strip_digits", dialpattern.strip_digits
                )
                dialpattern.prefix = kwargs.get("prefix", dialpattern.prefix)
                dialpattern.external_prefix = kwargs.get(
                    "external_prefix", dialpattern.external_prefix
                )
                dialpattern.caller_id = kwargs.get("caller_id", dialpattern.callerid)

    def _fix_context(self) -> None:
        """Fix the context based on associated extensions."""
        for extension in self.extensions:
            self.context = extension.context
            return
        self.context = None
