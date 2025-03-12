# file: accent_dao/models/meeting_authorization.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base
from accent_dao.helpers.datetime import utcnow_with_tzinfo

if TYPE_CHECKING:
    from .endpoint_sip import EndpointSIP
    from .meeting import Meeting


class MeetingAuthorization(Base):
    """Represents an authorization for a guest to join a meeting.

    Attributes:
        uuid: The unique identifier for the authorization.
        guest_uuid: The UUID of the guest.
        meeting_uuid: The UUID of the associated meeting.
        guest_name: The name of the guest.
        status: The status of the authorization.
        created_at: The timestamp when the authorization was created.
        meeting: Relationship to Meeting.
        guest_endpoint_sip: Relationship to EndpointSIP (via Meeting).

    """

    __tablename__: str = "meeting_authorization"
    __table_args__: tuple = (
        Index("meeting_authorization__idx__guest_uuid", "guest_uuid"),
        Index("meeting_authorization__idx__meeting_uuid", "meeting_uuid"),
    )

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4(), primary_key=True
    )
    guest_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    meeting_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("meeting.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    guest_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow_with_tzinfo,
        server_default=func.now(),
    )

    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        primaryjoin="Meeting.uuid == MeetingAuthorization.meeting_uuid",
        foreign_keys="MeetingAuthorization.meeting_uuid",
        viewonly=True,
    )
    guest_endpoint_sip: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP",
        secondary="meeting",
        secondaryjoin="EndpointSIP.uuid == Meeting.guest_endpoint_sip_uuid",
        primaryjoin="MeetingAuthorization.meeting_uuid == Meeting.uuid",
        viewonly=True,
        uselist=False,
    )
