# file: accent_dao/models/staticqueue.py
# Copyright 2025 Accent Communications

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class StaticQueue(Base):
    """Represents a static queue configuration entry.

    Attributes:
        id: The unique identifier for the static queue entry.
        cat_metric: The category metric.
        var_metric: The variable metric.
        commented: Indicates if the entry is commented out.
        filename: The filename associated with the entry.
        category: The category of the entry.
        var_name: The variable name.
        var_val: The variable value.

    """

    __tablename__: str = "staticqueue"
    __table_args__: tuple = (Index("staticqueue__idx__category", "category"),)

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    cat_metric: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    var_metric: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    filename: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    var_name: Mapped[str] = mapped_column(String(128), nullable=False)
    var_val: Mapped[str | None] = mapped_column(String(128), nullable=True)
