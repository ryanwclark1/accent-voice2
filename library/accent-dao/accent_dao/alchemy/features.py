# file: accent_dao/models/features.py
# Copyright 2025 Accent Communications

from sqlalchemy import Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class Features(Base):
    """Represents a feature.

    Attributes:
        id: The unique identifier for the feature.
        cat_metric: The category metric.
        var_metric: The variable metric.
        commented: Indicates if the feature is commented out.
        filename: The filename associated with the feature.
        category: The category of the feature.
        var_name: The variable name.
        var_val: The variable value.

    """

    __tablename__: str = "features"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        Index("features__idx__category", "category"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_metric: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    var_metric: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    filename: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    var_name: Mapped[str] = mapped_column(String(128), nullable=False)
    var_val: Mapped[str | None] = mapped_column(String(255), nullable=True)
