# src/accent_chatd/models/room.py

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Text, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_chatd.core.database import Base

if TYPE_CHECKING:
    from .room_message import RoomMessage  # prevent circular import
    from .room_user import RoomUser  # prevent circular import
    from .tenant import Tenant


class Room(Base):
    # __tablename__ defined in Base class
    # id = Column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(
        String, server_default=text("gen_random_uuid()"), primary_key=True
    )  # Use gen_random_uuid()
    name: Mapped[str | None] = mapped_column(Text)
    tenant_uuid: Mapped[int] = mapped_column(
        ForeignKey("chatd_tenant.id", ondelete="CASCADE"),
        nullable=False,  # Changed to ID.
    )

    users: Mapped[list["RoomUser"]] = relationship(
        "RoomUser", back_populates="room", cascade="all, delete-orphan"
    )
    messages: Mapped[list["RoomMessage"]] = relationship(
        "RoomMessage",
        back_populates="room",
        cascade="all, delete-orphan",
        order_by="desc(RoomMessage.created_at)",
    )

    __table_args__ = (Index("chatd_room__idx__tenant_uuid", "tenant_uuid"),)

    def __repr__(self) -> str:
        return f"Room(uuid={self.uuid!r}, name={self.name!r}, tenant_uuid={self.tenant_uuid!r})"
