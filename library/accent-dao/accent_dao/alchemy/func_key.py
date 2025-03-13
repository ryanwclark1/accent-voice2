# file: accent_dao/alchemy/func_key.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .func_key_destination_type import FuncKeyDestinationType
    from .func_key_mapping import FuncKeyMapping
    from .func_key_type import FuncKeyType


class FuncKey(Base):
    """Represents a function key.

    Attributes:
        id: The unique identifier for the function key.
        type_id: The ID of the associated function key type.
        destination_type_id: The ID of the destination type.
        func_key_type: Relationship to FuncKeyType.
        destination_type: Relationship to FuncKeyDestinationType.
        destination_type_name: The name of the destination type.
        func_key_mapping: Relationship to FuncKeyMapping.

    """

    __tablename__: str = "func_key"
    __table_args__: tuple = (Index("func_key__idx__type_id", "type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("func_key_type.id"), nullable=False
    )
    destination_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("func_key_destination_type.id"),
        primary_key=True,
    )

    func_key_type: Mapped["FuncKeyType"] = relationship(
        "FuncKeyType", foreign_keys=type_id
    )
    destination_type: Mapped["FuncKeyDestinationType"] = relationship(
        "FuncKeyDestinationType", foreign_keys=destination_type_id, viewonly=True
    )

    @property
    def destination_type_name(self) -> str:
        """Returns the name of the destination type.

        return: The name of the destination type.
        """
        return self.destination_type.name

    func_key_mapping: Mapped[list["FuncKeyMapping"]] = relationship(
        "FuncKeyMapping", cascade="all,delete-orphan"
    )
