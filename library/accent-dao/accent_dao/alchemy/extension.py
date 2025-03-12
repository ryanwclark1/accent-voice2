# file: accent_dao/models/extension.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Literal

from sqlalchemy import (
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import select

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .conference import Conference
    from .context import Context
    from .dialpattern import DialPattern
    from .groupfeatures import GroupFeatures
    from .incall import Incall
    from .line_extension import LineExtension
    from .parking_lot import ParkingLot
    from .queuefeatures import QueueFeatures


ExtenumbersType = Literal[
    "extenfeatures",
    "featuremap",
    "generalfeatures",
    "group",
    "incall",
    "outcall",
    "queue",
    "user",
    "voicemenu",
    "conference",
    "parking",
]


class Extension(Base):
    """Represents an extension.

    Attributes:
        id: The unique identifier for the extension.
        commented: Indicates if the extension is commented out.
        context: The context associated with the extension.
        exten: The extension number.
        type: The type of extension.
        typeval: The value associated with the extension type.
        context_rel: Relationship to Context.
        tenant_uuid: The UUID of the tenant.
        context_type: The type of the context.
        dialpattern: Relationship to DialPattern.
        outcall: Relationship to outcall.
        line_extensions: Relationship to LineExtension.
        lines: Lines this extension belongs to.
        group: Relationship to GroupFeatures.
        queue: Relationship to QueueFeatures.
        incall: Relationship to Incall.
        conference: Relationship to Conference.
        parking_lot: Relationship to ParkingLot.
        name: The name associated with the typeval.
        enabled: Indicates if the extension is enabled.

    """

    __tablename__: str = "extensions"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint("exten", "context"),
        Index("extensions__idx__context", "context"),
        Index("extensions__idx__exten", "exten"),
        Index("extensions__idx__type", "type"),
        Index("extensions__idx__typeval", "typeval"),
        ForeignKeyConstraint(
            ("context",),
            ("context.name",),
            ondelete="CASCADE",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    context: Mapped[str] = mapped_column(String(79), nullable=False, server_default="")
    exten: Mapped[str] = mapped_column(String(40), nullable=False, server_default="")
    type: Mapped[ExtenumbersType] = mapped_column(String, nullable=False)
    typeval: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")

    context_rel: Mapped["Context"] = relationship(
        "Context",
        primaryjoin="Extension.context == Context.name",
        foreign_keys="Extension.context",
    )

    @property
    def tenant_uuid(self) -> str | None:
        """The UUID of the tenant."""
        if self.context_rel:
            return self.context_rel.tenant_uuid

        return None

    @tenant_uuid.expression
    def tenant_uuid(cls) -> Mapped[str | None]:
        return (
            select(Context.tenant_uuid)
            .where(Context.name == cls.context)
            .scalar_subquery()
        )

    @property
    def context_type(self) -> str | None:
        if self.context_rel:
            return self.context_rel.contexttype
        return None

    @context_type.expression
    def context_type(cls) -> Mapped[str | None]:
        return (
            select(Context.contexttype)
            .where(Context.name == cls.context)
            .scalar_subquery()
        )

    dialpattern: Mapped["DialPattern"] = relationship(
        "DialPattern",
        primaryjoin="""and_(
            Extension.type == 'outcall',
            Extension.typeval == cast(DialPattern.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    @property
    def outcall(self) -> "DialPattern":
        return self.dialpattern

    line_extensions: Mapped[list["LineExtension"]] = relationship(
        "LineExtension", viewonly=True
    )

    @property
    def lines(self) -> list["LineExtension"]:
        return [le.linefeatures for le in self.line_extensions]

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            Extension.type == 'group',
            Extension.typeval == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="""and_(
            Extension.type == 'queue',
            Extension.typeval == cast(QueueFeatures.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    incall: Mapped["Incall"] = relationship(
        "Incall",
        primaryjoin="""and_(
            Extension.type == 'incall',
            Extension.typeval == cast(Incall.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    conference: Mapped["Conference"] = relationship(
        "Conference",
        primaryjoin="""and_(
            Extension.type == 'conference',
            Extension.typeval == cast(Conference.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    parking_lot: Mapped["ParkingLot"] = relationship(
        "ParkingLot",
        primaryjoin="""and_(
            Extension.type == 'parking',
            Extension.typeval == cast(ParkingLot.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    @property
    def name(self) -> str:
        """The name associated with the typeval."""
        return self.typeval

    @property
    def enabled(self) -> bool:
        """Indicates if the extension is enabled."""
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disables the extension."""
        self.commented = int(not value)

    def is_pattern(self) -> bool:
        """Checks if the extension is a pattern (starts with '_')."""
        return self.exten.startswith("_")

    def get_old_context(self):
        """Legacy support to get old contexts."""
        context_history = get_history(self, "context")
        if context_history[2]:
            return context_history[2][0]
        return self.context
