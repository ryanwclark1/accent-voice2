# file: accent_dao/models/func_key_destination_type.py
# Copyright 2025 Accent Communications
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class FuncKeyDestinationType(Base):
    """Represents a function key destination type.

    Attributes:
        id: The unique identifier for the destination type.
        name: The name of the destination type.

    """

    __tablename__: str = "func_key_destination_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    @classmethod
    def query_id(cls, name: str) -> Mapped[int]:
        """Query the ID of a destination type by its name."""
        return select(cls.id).where(cls.name == name)
