# file: accent_dao/alchemy/parking_lot.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import select

from accent_dao.helpers.db_manager import Base

from .extension import Extension

if TYPE_CHECKING:
    from .func_key_dest_park_position import FuncKeyDestParkPosition
    from .func_key_dest_parking import FuncKeyDestParking


class ParkingLot(Base):
    """Represents a parking lot.

    Attributes:
        id: The unique identifier for the parking lot.
        tenant_uuid: The UUID of the tenant the parking lot belongs to.
        name: The name of the parking lot.
        slots_start: The starting slot number.
        slots_end: The ending slot number.
        timeout: The timeout for parked calls.
        music_on_hold: The music on hold setting.
        extensions: Relationship to Extension.
        func_keys_park_position: Relationship to FuncKeyDestParkPosition.
        func_keys_parking: Relationship to FuncKeyDestParking.
        exten: The extension number of the parking lot.
        context: The context of the parking lot.

    """

    __tablename__: str = "parking_lot"
    __table_args__: tuple = (Index("parking_lot__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    slots_start: Mapped[str] = mapped_column(String(40), nullable=False)
    slots_end: Mapped[str] = mapped_column(String(40), nullable=False)
    timeout: Mapped[int | None] = mapped_column(Integer, nullable=True)
    music_on_hold: Mapped[str | None] = mapped_column(String(128), nullable=True)

    extensions: Mapped[list["Extension"]] = relationship(
        "Extension",
        primaryjoin="""and_(
            Extension.type == 'parking',
            Extension.typeval == cast(ParkingLot.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    func_keys_park_position: Mapped[list["FuncKeyDestParkPosition"]] = relationship(
        "FuncKeyDestParkPosition", cascade="all, delete-orphan"
    )

    func_keys_parking: Mapped[list["FuncKeyDestParking"]] = relationship(
        "FuncKeyDestParking", cascade="all, delete-orphan"
    )

    def in_slots_range(self, exten: str | int) -> bool:
        """Check if an extension is within the parking lot's slots range.

        Args:
            exten: The extension to check.

        Returns:
            True if the extension is in range, False otherwise.

        """
        if not str(exten).isdigit() or str(exten).startswith("0"):
            return False

        exten = int(exten)
        start = int(self.slots_start)
        end = int(self.slots_end)

        return start <= exten <= end

    @property
    def exten(self) -> str | None:
        """The extension number of the parking lot."""
        for extension in self.extensions:
            return extension.exten
        return None

    @exten.setter
    def exten(self, value: str) -> None:
        """There is no setter, you can't set the extension directly."""

    @exten.expression
    def exten(cls) -> Mapped[str | None]:
        """Retrieve the extension value for a parking lot.

        This method constructs a SQL query to select the `exten` field from the
        `Extension` table where the `type` is "parking" and the `typeval`
        matches the string representation of the class instance's `id`.

        Returns:
            Mapped[str | None]: A scalar subquery that returns the extension
                    value as a string, or None if no matching record is found.

        """
        return (
            select(Extension.exten)
            .where(Extension.type == "parking")
            .where(Extension.typeval == func.cast(cls.id, String))
            .scalar_subquery()
        )

    @property
    def context(self) -> str | None:
        """The context of the parking lot."""
        for extension in self.extensions:
            return extension.context
        return None

    @context.setter
    def context(self, value: str) -> None:
        """There is no setter, you can't set the context directly."""

    @context.expression
    def context(cls) -> Mapped[str | None]:
        """Return a SQLAlchemy scalar subquery.

        Subquery selects the context of an extension where the extension type is
        "parking" and the typeval matches the string representation of the
        class's id

        Returns:
            Mapped[str | None]: A scalar subquery selecting the context.

        """
        return (
            select(Extension.context)
            .where(Extension.type == "parking")
            .where(Extension.typeval == func.cast(cls.id, String))
            .scalar_subquery()
        )
