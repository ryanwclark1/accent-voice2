# src/accent_chatd/models/endpoint.py

from sqlalchemy import CheckConstraint, Column, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_chatd.core.database import Base


class Endpoint(Base):
    # __tablename__ defined in Base class
    # id = Column(Integer, primary_key=True) # Defined in Base class
    name: Mapped[str] = mapped_column(Text, primary_key=True)
    state: Mapped[str] = mapped_column(
        String(24),
        CheckConstraint("state in ('available', 'unavailable')"),
        nullable=False,
        default="unavailable",
    )

    line: Mapped["Line"] = relationship(
        "Line", back_populates="endpoint", uselist=False
    )  # One-to-one

    def __repr__(self) -> str:
        return f"Endpoint(id={self.id!r},name={self.name!r}, state={self.state!r})"
