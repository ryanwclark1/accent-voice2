# file: accent_dao/alchemy/func_key_dest_park_position.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    cast,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .func_key import FuncKey
    from .parking_lot import ParkingLot


class FuncKeyDestParkPosition(Base):
    """Represents a function key destination for a parking lot position.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 7).
        parking_lot_id: The ID of the associated parking lot.
        park_position: The parking position (as a string).
        type: The type of destination ('park_position').
        func_key: Relationship to FuncKey.
        parking_lot: Relationship to ParkingLot.
        position: The parking position (as an integer).

    """

    DESTINATION_TYPE_ID: int = 7

    __tablename__: str = "func_key_dest_park_position"
    __table_args__: tuple = (
        PrimaryKeyConstraint("func_key_id", "destination_type_id"),
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        UniqueConstraint("parking_lot_id", "park_position"),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
        CheckConstraint("park_position ~ '^[0-9]+$'"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )
    parking_lot_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("parking_lot.id"), nullable=False
    )
    park_position: Mapped[str] = mapped_column(String(40), nullable=False)

    type: str = "park_position"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    parking_lot: Mapped["ParkingLot"] = relationship("ParkingLot")

    def to_tuple(self) -> tuple[tuple[str, int], tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (
            ("parking_lot_id", self.parking_lot_id),
            ("position", self.position),
        )

    @property
    def position(self) -> int:
        """The parking position (as an integer)."""
        return int(self.park_position)

    @position.setter
    def position(self, value: int | str) -> None:
        """Set the parking position."""
        self.park_position = str(value)  # Ensure string

    @position.expression
    def position(cls) -> Mapped[int]:
        return cast(cls.park_position, Integer)
