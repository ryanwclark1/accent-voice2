# file: accent_dao/models/meeting.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.datetime import utcnow_with_tzinfo

if TYPE_CHECKING:
    from .endpoint_sip import EndpointSIP
    from .ingress_http import IngressHTTP
    from .meeting_authorization import MeetingAuthorization
    from .userfeatures import UserFeatures


class MeetingOwner(Base):
    """Represents an owner of a meeting.

    Attributes:
        meeting_uuid: The UUID of the associated meeting.
        user_uuid: The UUID of the associated user.
        owner: Relationship to the UserFeatures model.

    """

    __tablename__: str = "meeting_owner"

    meeting_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("meeting.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    user_uuid: Mapped[str] = mapped_column(
        String(38),  # 38 is copied from userfeatures.uuid
        ForeignKey("userfeatures.uuid", ondelete="CASCADE"),
        primary_key=True,
    )

    owner: Mapped["UserFeatures"] = relationship(
        "UserFeatures", foreign_keys="MeetingOwner.user_uuid"
    )


class Meeting(Base):
    """Represents a meeting.

    Attributes:
        uuid: The unique identifier for the meeting.
        name: The name of the meeting.
    guest_endpoint_sip_uuid: The UUID of the guest SIP endpoint (if applicable).
        tenant_uuid: The UUID of the tenant the meeting belongs to.
        created_at: The timestamp when the meeting was created.
        persistent: Indicates if the meeting is persistent.
        number: The meeting number.
        require_authorization: Indicates if authorization is required to join.
        meeting_owners: Relationship to MeetingOwner.
        owners: The owners of the meeting.
        guest_endpoint_sip: Relationship to EndpointSIP.
        ingress_http: Relationship to IngressHTTP.
        meeting_authorizations: Relationship to MeetingAuthorization.
        owner_uuids: A list of UUIDs of the meeting owners.

    """

    __tablename__: str = "meeting"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4(), primary_key=True
    )
    name: Mapped[str | None] = mapped_column(Text, nullable=True)
    guest_endpoint_sip_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoint_sip.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow_with_tzinfo,
        server_default=func.now(),
    )  # Keep server default
    persistent: Mapped[bool] = mapped_column(
        Boolean, server_default="false", nullable=False
    )  # Keep server default
    number: Mapped[str] = mapped_column(Text, nullable=False)
    require_authorization: Mapped[bool] = mapped_column(
        Boolean, server_default="false", nullable=False
    )  # Keep server default

    meeting_owners: Mapped[list["MeetingOwner"]] = relationship(
        "MeetingOwner",
        cascade="all, delete-orphan",
    )

    @property
    def owners(self) -> list["MeetingOwner"]:
        return [o.owner for o in self.meeting_owners]

    @owners.setter
    def owners(self, value: list["MeetingOwner"]) -> None:
        self.meeting_owners = [MeetingOwner(owner=v) for v in value]

    guest_endpoint_sip: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    ingress_http: Mapped["IngressHTTP"] = relationship(
        "IngressHTTP",
        foreign_keys="IngressHTTP.tenant_uuid",
        uselist=False,
        viewonly=True,
        primaryjoin="Meeting.tenant_uuid == IngressHTTP.tenant_uuid",
    )
    meeting_authorizations: Mapped[list["MeetingAuthorization"]] = relationship(
        "MeetingAuthorization",
        primaryjoin="MeetingAuthorization.meeting_uuid == Meeting.uuid",
        foreign_keys="MeetingAuthorization.meeting_uuid",
        cascade="all, delete-orphan",
    )

    @property
    def owner_uuids(self) -> list[UUID]:
        """A list of UUIDs of the meeting owners."""
        return [owner.uuid for owner in self.owners]
