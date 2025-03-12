# file: accent_dao/models/application_dest_node.py
# Copyright 2025 Accent Communications

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class ApplicationDestNode(Base):
    """Represents a destination node for an application.

    Attributes:
        application_uuid: The UUID of the application.
        type_: The type of destination node ('holding' or 'mixing').
        music_on_hold: The music on hold setting.
        answer: Indicates if the call should be answered.

    """

    __tablename__: str = "application_dest_node"

    application_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("application.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    type_: Mapped[str] = mapped_column(
        "type",
        String(32),
        CheckConstraint("type in ('holding', 'mixing')"),
        nullable=False,
    )
    music_on_hold: Mapped[str | None] = mapped_column(String(128), nullable=True)
    answer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
