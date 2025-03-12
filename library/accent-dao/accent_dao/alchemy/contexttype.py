# file: accent_dao/models/contexttype.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class ContextType(Base):
    """Represents a context type.

    Attributes:
        id: The unique identifier for the context type.
        name: The name of the context type.
        commented: Indicates if the context type is commented out.
        deletable: Indicates if the context type is deletable.
        description: A description of the context type.

    """

    __tablename__: str = "contexttype"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    commented: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deletable: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
