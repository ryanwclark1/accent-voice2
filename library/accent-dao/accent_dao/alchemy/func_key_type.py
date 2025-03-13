# file: accent_dao/alchemy/func_key_type.py
# Copyright 2025 Accent Communications


from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class FuncKeyType(Base):
    """Represents a function key type.

    Attributes:
        id: The unique identifier for the function key type.
        name: The name of the function key type.

    """

    __tablename__: str = "func_key_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    @classmethod
    def query_id(cls, name: str) -> Mapped[int]:
        """Query the ID of a function key type by its name."""
        return select(cls.id).where(cls.name == name)
