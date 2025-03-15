# src/accent_chatd/models/channel.py
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_chatd.core.database import Base

if TYPE_CHECKING:
    from .line import Line  # prevent circular import


class Channel(Base):
    # __tablename__ defined in Base class
    # id = Column(Integer, primary_key=True) # Defined in Base class
    name: Mapped[str] = mapped_column(Text, primary_key=True)
    state: Mapped[str] = mapped_column(
        String(24),
        CheckConstraint(
            "state in ('undefined', 'holding', 'ringing', 'talking', 'progressing')"  # added progressing
        ),
        nullable=False,
        default="undefined",
    )
    line_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chatd_line.id", ondelete="CASCADE"), nullable=False
    )

    line: Mapped["Line"] = relationship("Line", back_populates="channels")
    __table_args__ = (Index("chatd_channel__idx__line_id", "line_id"),)

    def __repr__(self) -> str:
        return f"Channel(id={self.id!r}, name={self.name!r}, state={self.state!r}, line_id={self.line_id!r})"
