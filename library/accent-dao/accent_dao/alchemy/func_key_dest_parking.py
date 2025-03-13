# file: accent_dao/alchemy/func_key_dest_parking.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .func_key import FuncKey
    from .parking_lot import ParkingLot


class FuncKeyDestParking(Base):
    """Represents a function key destination for a parking lot.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 14).
        parking_lot_id: The ID of the associated parking lot.
        type: The type of destination ('parking').
        func_key: Relationship to FuncKey.
        parking_lot: Relationship to ParkingLot.

    """

    DESTINATION_TYPE_ID: int = 14

    __tablename__: str = "func_key_dest_parking"
    __table_args__: tuple = (
        PrimaryKeyConstraint("func_key_id", "destination_type_id"),
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )
    parking_lot_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("parking_lot.id"),
        nullable=False,
        unique=True,
    )

    type: str = "parking"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    parking_lot: Mapped["ParkingLot"] = relationship("ParkingLot")

    def to_tuple(self) -> tuple[tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (("parking_lot_id", self.parking_lot_id),)
