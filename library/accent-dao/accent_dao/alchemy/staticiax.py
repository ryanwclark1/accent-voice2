# file: accent_dao/alchemy/staticiax.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import cast
from sqlalchemy.sql.expression import ColumnElement  # Import ColumnElement

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .trunkfeatures import TrunkFeatures


class StaticIAX(Base):
    """Represents a static IAX configuration entry.

    Attributes:
        id: The unique identifier for the IAX entry.
        cat_metric: The category metric.
        var_metric: The variable metric.
        commented: Indicates if the entry is commented out.
        filename: The filename associated with the entry.
        category: The category of the entry.
        var_name: The variable name.
        var_val: The variable value.
        trunk: Relationship to TrunkFeatures.
        metric: The metric (var_metric + 1, or None if var_metric is 0).
        enabled: Indicates if the entry is enabled.

    """

    __tablename__: str = "staticiax"
    __table_args__: tuple = (Index("staticiax__idx__category", "category"),)

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    cat_metric: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    var_metric: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    filename: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    var_name: Mapped[str] = mapped_column(String(128), nullable=False)
    var_val: Mapped[str | None] = mapped_column(Text, nullable=True)  # Changed to Text

    trunk: Mapped["TrunkFeatures"] = relationship(
        "TrunkFeatures", viewonly=True, uselist=False
    )

    @property
    def metric(self) -> int | None:
        """The metric (var_metric + 1, or None if var_metric is 0)."""
        if self.var_metric == 0:
            return None
        return self.var_metric + 1

    @metric.setter
    def metric(self, value: int | None) -> None:
        """Set the metric."""
        if value is None:
            self.var_metric = 0
        else:
            self.var_metric = value - 1  # Modified

    @metric.expression  # type: ignore[no-redef]
    def metric(cls) -> ColumnElement[int | None]:
        """Return the metric expression."""
        return func.nullif(cls.var_metric, 0)

    @property
    def enabled(self) -> bool | None:
        """Indicates if the entry is enabled."""
        if self.commented is None:
            return None
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        """Enable or disable the entry."""
        self.commented = int(not value) if value is not None else None

    @enabled.expression  # type: ignore[no-redef]
    def enabled(cls) -> ColumnElement[bool]:  # Corrected return type
        """Return the enabled expression."""
        return func.not_(cast(cls.commented, Boolean))
