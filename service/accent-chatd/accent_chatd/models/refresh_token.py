# src/accent_chatd/models/line.py

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Text, Index
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_chatd.core.database import Base

if TYPE_CHECKING:
    from .channel import Channel  # prevent circular import
    from .endpoint import Endpoint  # prevent circular import
    from .user import User


class Line(Base):
    # __tablename__ defined in Base class
    id: Mapped[int] = mapped_column(primary_key=True)  # Use Mapped for type hinting
    user_uuid: Mapped[int] = mapped_column(
        ForeignKey("chatd_user.id", ondelete="CASCADE")
    )
    endpoint_name: Mapped[str | None] = mapped_column(
        Text, ForeignKey("chatd_endpoint.name", ondelete="SET NULL")
    )
    media: Mapped[str | None] = mapped_column(
        String(24), CheckConstraint("media in ('audio', 'video')")
    )

    user: Mapped["User"] = relationship("User", back_populates="lines")
    endpoint: Mapped["Endpoint"] = relationship("Endpoint", back_populates="line")
    channels: Mapped[list["Channel"]] = relationship(
        "Channel", back_populates="line", cascade="all, delete-orphan"
    )

    # Association proxies
    tenant_uuid = association_proxy("user", "tenant_uuid")
    endpoint_state = association_proxy("endpoint", "state")
    channels_state = association_proxy("channels", "state")
    __table_args__ = (
        Index("chatd_line__idx__user_uuid", "user_uuid"),
        Index("chatd_line__idx__endpoint_name", "endpoint_name"),
    )

    def __repr__(self) -> str:
        return f"Line(id={self.id!r}, user_uuid={self.user_uuid!r}, endpoint_name={self.endpoint_name!r}, media={self.media!r})"
