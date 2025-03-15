# src/accent_chatd/models/room_user.py

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_chatd.core.database import Base

if TYPE_CHECKING:
    from .room import Room  # prevent circular imports


class RoomUser(Base):
    # __tablename__ defined in Base class
    # id = Column(Integer, primary_key=True) # Defined in Base class
    room_uuid: Mapped[int] = mapped_column(
        ForeignKey("chatd_room.id", ondelete="CASCADE"),
        primary_key=True,  # Change to id.
    )
    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(String, primary_key=True)
    accent_uuid: Mapped[str] = mapped_column(String, primary_key=True)

    room: Mapped["Room"] = relationship("Room", back_populates="users")

    def __repr__(self) -> str:
        return f"RoomUser(room_uuid={self.room_uuid!r}, uuid={self.uuid!r}, tenant_uuid={self.tenant_uuid!r}, accent_uuid={self.accent_uuid!r})"
