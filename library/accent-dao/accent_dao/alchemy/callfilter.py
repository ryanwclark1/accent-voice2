# file: accent_dao/alchemy/callfilter.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Literal, get_args

from sqlalchemy import (
    Enum,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship
from sqlalchemy.sql import and_, select

from accent_dao.helpers.db_manager import Base

from .callerid import Callerid, CalleridMode
from .feature_extension import FeatureExtension

# Add these for clarity and type safety
CallfilterType = Literal["bosssecretary"]
CallfilterBosssecretary = Literal[
    "bossfirst-serial",
    "bossfirst-simult",
    "secretary-serial",
    "secretary-simult",
    "all",
]
CallfilterCallfrom = Literal["internal", "external", "all"]

if TYPE_CHECKING:
    from .callfiltermember import Callfiltermember
    from .dialaction import Dialaction


def _convert_to_bosssecretary(value: str) -> CallfilterBosssecretary | str:
    """Convert a string to a CallfilterBosssecretary enum member, if possible.

    Args:
        value: The string value to convert.

    Returns:
        CallfilterBosssecretary | str: The enum member if valid, or
        the original string if not.

    """
    if value in get_args(CallfilterBosssecretary):
        return value  # type: ignore #  mypy is confused, but this is correct.
    return value


class Callfilter(Base):
    """Represents a call filter.

    Attributes:
        id: The unique identifier for the call filter.
        tenant_uuid: The UUID of the tenant the call filter belongs to.
        name: The name of the call filter.
        type: The type of call filter ('bosssecretary').
        bosssecretary: The boss-secretary strategy.
        callfrom: Specifies from where calls are filtered.
        ringseconds: The number of seconds to ring.
        commented: Indicates if the call filter is commented out.
        description: A description of the call filter.
        exten: A computed property for the extension.
        callfilter_dialactions: Relationship to Dialaction, mapped by event.
        caller_id: Relationship to Callerid.
        caller_id_mode: The caller ID mode.
        caller_id_name: The caller ID name.
        recipients: Relationship to Callfiltermember (bosses).
        surrogates: Relationship to Callfiltermember (secretaries).
        fallbacks:  The fallback dialactions.
        strategy: The call filter strategy.
        surrogates_timeout: The timeout for surrogates.
        enabled: Indicates if the call filter is enabled.

    """

    __tablename__: str = "callfilter"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint("name"),
        Index("callfilter__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    type: Mapped[CallfilterType] = mapped_column(
        Enum("bosssecretary", name="callfilter_type"), nullable=False
    )
    bosssecretary: Mapped[CallfilterBosssecretary | None] = mapped_column(
        Enum(
            "bossfirst-serial",
            "bossfirst-simult",
            "secretary-serial",
            "secretary-simult",
            "all",
            name="callfilter_bosssecretary",
        ),
        nullable=True,
    )
    callfrom: Mapped[CallfilterCallfrom | None] = mapped_column(
        Enum("internal", "external", "all", name="callfilter_callfrom"), nullable=True
    )
    ringseconds: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    exten: Mapped[str] = column_property(
        select(FeatureExtension.exten)
        .where(
            and_(
                FeatureExtension.feature == "bsfilter",
                FeatureExtension.enabled.is_(True),  # Use SQLAlchemy's is_()
            )
        )
        .scalar_subquery()
    )

    # Removed collection_class=attribute_mapped_collection('event')
    callfilter_dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'callfilter',
            Dialaction.categoryval == cast(Callfilter.id, String)
        )""",
        cascade="all, delete-orphan",
        foreign_keys="Dialaction.categoryval",
    )

    caller_id: Mapped["Callerid"] = relationship(
        "Callerid",
        primaryjoin="""and_(
            Callerid.type == 'callfilter',
            Callerid.typeval == Callfilter.id
        )""",
        foreign_keys="Callerid.typeval",
        cascade="all, delete-orphan",
        uselist=False,
    )

    # These are now regular properties, setting attributes.
    @property
    def caller_id_mode(self) -> str | None:  # noqa: D102
        return self.caller_id.mode if self.caller_id else None

    @caller_id_mode.setter
    def caller_id_mode(self, value: CalleridMode) -> None:  # Correct type hint
        if self.caller_id:
            self.caller_id.mode = value
        else:
            self.caller_id = Callerid(type="callfilter", mode=value)

    @property
    def caller_id_name(self) -> str | None:
        """Retrieves the caller ID name.

        Returns:
            str | None: The name associated with the caller ID if it exists,
                otherwise None.

        """
        return self.caller_id.name if self.caller_id else None

    @caller_id_name.setter
    def caller_id_name(self, value: str | None) -> None:
        if self.caller_id:
            self.caller_id.name = value
        else:
            self.caller_id = Callerid(type="callfilter", name=value)  # type: ignore

    recipients: Mapped[list["Callfiltermember"]] = relationship(
        "Callfiltermember",
        primaryjoin="""and_(
            Callfiltermember.bstype == 'boss',
            Callfiltermember.callfilterid == Callfilter.id
        )""",
        foreign_keys="Callfiltermember.callfilterid",
        order_by="Callfiltermember.priority",
        collection_class=ordering_list("priority", reorder_on_append=True),
        cascade="all, delete-orphan",
    )

    surrogates: Mapped[list["Callfiltermember"]] = relationship(
        "Callfiltermember",
        primaryjoin="""and_(
            Callfiltermember.bstype == 'secretary',
            Callfiltermember.callfilterid == Callfilter.id
        )""",
        foreign_keys="Callfiltermember.callfilterid",
        order_by="Callfiltermember.priority",
        collection_class=ordering_list("priority", reorder_on_append=True),
        cascade="all, delete-orphan",
    )

    @property
    def fallbacks(self) -> dict[str, "Dialaction"]:
        """Get the fallback dialactions for the call filter."""
        return self.callfilter_dialactions

    @property
    def strategy(self) -> str:
        """Get the call filter strategy."""
        # Handle the case where bosssecretary is a string
        if isinstance(self.bosssecretary, str):
            return self.bosssecretary
        if self.bosssecretary == "bossfirst-serial":
            return "all-recipients-then-linear-surrogates"
        if self.bosssecretary == "bossfirst-simult":
            return "all-recipients-then-all-surrogates"
        if self.bosssecretary == "secretary-serial":
            return "linear-surrogates-then-all-recipients"
        if self.bosssecretary == "secretary-simult":
            return "all-surrogates-then-all-recipients"
        return self.bosssecretary or "all"  # Added default

    @strategy.setter
    def strategy(self, value: str) -> None:
        """Set the call filter strategy.

        Args:
            value: strategy name

        """
        self.bosssecretary = _convert_to_bosssecretary(value)

    @property
    def surrogates_timeout(self) -> int | None:
        """Get the timeout for surrogates (in seconds)."""
        if self.ringseconds == 0:
            return None
        return self.ringseconds

    @surrogates_timeout.setter
    def surrogates_timeout(self, value: int | None) -> None:
        """Set the timeout for surrogates.

        Args:
            value: int or None

        """
        if value is None:
            self.ringseconds = 0
        else:
            self.ringseconds = value

    @property
    def enabled(self) -> bool:
        """Indicate if the call filter is enabled."""
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disables the call filter."""
        self.commented = int(not value)
