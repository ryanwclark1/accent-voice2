# src/accent_chatd/models/user.py

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_chatd.core.database import Base

if TYPE_CHECKING:
    from .line import Line  # prevent circular import
    from .refresh_token import RefreshToken  # prevent circular import
    from .session import Session  # prevent circular import
    from .tenant import Tenant


class User(Base):
    # __tablename__ defined in Base
    # id = Column(Integer, primary_key=True)  # Auto-incrementing surrogate key
    id: Mapped[int] = mapped_column(primary_key=True)  # Use Mapped for type hinting
    uuid: Mapped[str] = mapped_column(String)  # Keep the UUID, but use string
    tenant_uuid: Mapped[int] = mapped_column(
        ForeignKey("chatd_tenant.id", ondelete="CASCADE"),
        nullable=False,  # Changed to ID.
    )
    state: Mapped[str] = mapped_column(
        String(24),
        CheckConstraint(
            "state in ('available', 'unavailable', 'invisible', 'away')"
        ),  # Keep options
        nullable=False,
    )
    status: Mapped[str | None] = mapped_column(Text, nullable=True)
    do_not_disturb: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    last_activity: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    tenant: Mapped["Tenant"] = relationship("Tenant")  # Relationship to Tenant
    sessions: Mapped[list["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )
    lines: Mapped[list["Line"]] = relationship(
        "Line", back_populates="user", cascade="all, delete-orphan"
    )
    __table_args__ = (Index("chatd_user__idx__tenant_uuid", "tenant_uuid"),)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, uuid={self.uuid!r}, tenant_uuid={self.tenant_uuid!r}, state={self.state!r}, status={self.status!r}, do_not_disturb={self.do_not_disturb!r}, last_activity={self.last_activity!r})"
