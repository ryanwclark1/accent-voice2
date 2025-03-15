# src/accent_chatd/models/session.py
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Index
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_chatd.core.database import Base

if TYPE_CHECKING:
    from .user import User  # prevent circular import


class Session(Base):
    # __tablename__ defined in Base class
    # id = Column(Integer, primary_key=True) # Defined in base class
    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    mobile: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_uuid: Mapped[int] = mapped_column(
        ForeignKey("chatd_user.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    tenant_uuid = association_proxy("user", "tenant_uuid")
    __table_args__ = (Index("chatd_session__idx__user_uuid", "user_uuid"),)

    def __repr__(self) -> str:
        return f"Session(uuid={self.uuid!r}, mobile={self.mobile!r}, user_uuid={self.user_uuid!r})"
