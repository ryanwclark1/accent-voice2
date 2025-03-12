# file: accent_dao/models/context.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .contextinclude import ContextInclude
    from .contextnumbers import ContextNumbers
    from .tenant import Tenant


class Context(Base):
    """Represents a context.

    Attributes:
        id: The unique identifier for the context.
        uuid: A unique UUID for the context.
        tenant_uuid: The UUID of the tenant the context belongs to.
        name: The name of the context.
        displayname: The display name of the context.
        contexttype: The type of context ('internal' by default).
        commented: Indicates if the context is commented out.
        description: A description of the context.
        context_numbers_user: Relationship to ContextNumbers for user ranges.
        context_numbers_group: Relationship to ContextNumbers for group ranges.
        context_numbers_queue: Relationship to ContextNumbers for queue ranges.
        context_numbers_meetme: Relationship to ContextNumbers for conference room ranges.
        context_numbers_incall: Relationship to ContextNumbers for incall ranges.
        context_includes_children: Relationship to child ContextIncludes.
        context_include_parents: Relationship to parent ContextIncludes.
        contexts: Included contexts.
        tenant: Relationship to Tenant.
        label: The display name of the context.
        type: The type of the context.
        enabled: Indicates if the context is enabled.
        user_ranges: The user number ranges.
        group_ranges: The group number ranges.
        queue_ranges: The queue number ranges.
        conference_room_ranges: The conference room number ranges.
        incall_ranges: The incall number ranges.

    """

    __tablename__: str = "context"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint("name"),
        UniqueConstraint("uuid"),
        ForeignKeyConstraint(
            ("tenant_uuid",),
            ("tenant.uuid",),
            ondelete="CASCADE",
        ),
        Index("context__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4()
    )
    tenant_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    name: Mapped[str] = mapped_column(String(79), nullable=False)
    displayname: Mapped[str | None] = mapped_column(String(128), nullable=True)
    contexttype: Mapped[str] = mapped_column(
        String(40), nullable=False, server_default="internal"
    )
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    context_numbers_user: Mapped[list["ContextNumbers"]] = relationship(
        "ContextNumbers",
        primaryjoin="""and_(
            ContextNumbers.type == 'user',
            ContextNumbers.context == Context.name)""",
        foreign_keys="ContextNumbers.context",
        cascade="all, delete-orphan",
    )

    context_numbers_group: Mapped[list["ContextNumbers"]] = relationship(
        "ContextNumbers",
        primaryjoin="""and_(
            ContextNumbers.type == 'group',
            ContextNumbers.context == Context.name)""",
        foreign_keys="ContextNumbers.context",
        cascade="all, delete-orphan",
    )

    context_numbers_queue: Mapped[list["ContextNumbers"]] = relationship(
        "ContextNumbers",
        primaryjoin="""and_(
            ContextNumbers.type == 'queue',
            ContextNumbers.context == Context.name)""",
        foreign_keys="ContextNumbers.context",
        cascade="all, delete-orphan",
    )

    context_numbers_meetme: Mapped[list["ContextNumbers"]] = relationship(
        "ContextNumbers",
        primaryjoin="""and_(
            ContextNumbers.type == 'meetme',
            ContextNumbers.context == Context.name)""",
        foreign_keys="ContextNumbers.context",
        cascade="all, delete-orphan",
    )

    context_numbers_incall: Mapped[list["ContextNumbers"]] = relationship(
        "ContextNumbers",
        primaryjoin="""and_(
            ContextNumbers.type == 'incall',
            ContextNumbers.context == Context.name)""",
        foreign_keys="ContextNumbers.context",
        cascade="all, delete-orphan",
    )

    context_includes_children: Mapped[list["ContextInclude"]] = relationship(
        "ContextInclude",
        primaryjoin="ContextInclude.include == Context.name",
        foreign_keys="ContextInclude.include",
        cascade="all, delete-orphan",
    )

    context_include_parents: Mapped[list["ContextInclude"]] = relationship(
        "ContextInclude",
        primaryjoin="ContextInclude.context == Context.name",
        foreign_keys="ContextInclude.context",
        order_by="ContextInclude.priority",
        collection_class=ordering_list("priority", reorder_on_append=True),
        cascade="all, delete-orphan",
    )

    @property
    def contexts(self) -> list[str]:
        """Returns a list of included contexts."""
        return [p.included_context for p in self.context_include_parents]

    @contexts.setter
    def contexts(self, value: list[str]) -> None:
        """Set the included contexts."""
        self.context_include_parents = [
            ContextInclude(included_context=v) for v in value
        ]

    tenant: Mapped["Tenant"] = relationship("Tenant", viewonly=True)

    @property
    def label(self) -> str | None:
        """The label (display name) of the context."""
        return self.displayname

    @label.setter
    def label(self, value: str | None) -> None:
        """Set the label (display name) of the context."""
        self.displayname = value

    @property
    def type(self) -> str:
        """The type of the context."""
        return self.contexttype

    @type.setter
    def type(self, value: str) -> None:
        """Set the type of the context."""
        self.contexttype = value

    @property
    def enabled(self) -> bool:
        """Indicates if the context is enabled."""
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disables the context."""
        self.commented = int(not value)

    @property
    def user_ranges(self) -> list["ContextNumbers"]:
        """The user number ranges."""
        return self.context_numbers_user

    @user_ranges.setter
    def user_ranges(self, user_ranges: list["ContextNumbers"]) -> None:
        """Set the user number ranges."""
        for user_range in user_ranges:
            user_range.type = "user"
        self.context_numbers_user = user_ranges

    @property
    def group_ranges(self) -> list["ContextNumbers"]:
        """The group number ranges."""
        return self.context_numbers_group

    @group_ranges.setter
    def group_ranges(self, group_ranges: list["ContextNumbers"]) -> None:
        """Set the group number ranges."""
        for group_range in group_ranges:
            group_range.type = "group"
        self.context_numbers_group = group_ranges

    @property
    def queue_ranges(self) -> list["ContextNumbers"]:
        """The queue number ranges."""
        return self.context_numbers_queue

    @queue_ranges.setter
    def queue_ranges(self, queue_ranges: list["ContextNumbers"]) -> None:
        """Set the queue number ranges."""
        for queue_range in queue_ranges:
            queue_range.type = "queue"
        self.context_numbers_queue = queue_ranges

    @property
    def conference_room_ranges(self) -> list["ContextNumbers"]:
        """The conference room number ranges."""
        return self.context_numbers_meetme

    @conference_room_ranges.setter
    def conference_room_ranges(
        self, conference_room_ranges: list["ContextNumbers"]
    ) -> None:
        """Set the conference room number ranges."""
        for conference_room_range in conference_room_ranges:
            conference_room_range.type = "meetme"
        self.context_numbers_meetme = conference_room_ranges

    @property
    def incall_ranges(self) -> list["ContextNumbers"]:
        """The incall number ranges."""
        return self.context_numbers_incall

    @incall_ranges.setter
    def incall_ranges(self, incall_ranges: list["ContextNumbers"]) -> None:
        """Set the incall number ranges."""
        for incall_range in incall_ranges:
            incall_range.type = "incall"
        self.context_numbers_incall = incall_ranges
