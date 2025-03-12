# file: accent_dao/models/tenant.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .endpoint_sip import EndpointSIP


class Tenant(Base):
    """Represents a tenant.

    Attributes:
        uuid: The unique identifier for the tenant.
        slug: A short, URL-friendly identifier for the tenant.
        sip_templates_generated: Indicates if SIP templates have been generated.
    global_sip_template_uuid: The UUID of the global SIP template (if applicable).
    webrtc_sip_template_uuid: The UUID of the WebRTC SIP template (if applicable).
    registration_trunk_sip_template_uuid: The UUID of the registration
    trunk SIP template.
    meeting_guest_sip_template_uuid: The UUID of the meeting guest SIP template
    twilio_trunk_sip_template_uuid: The UUID of the twilio SIP template
        global_sip_template: Relationship to the global EndpointSIP template.
        webrtc_sip_template: Relationship to the WebRTC EndpointSIP template.
    registration_trunk_sip_template: Relationship to registration trunk
    EndpointSIP template.
        meeting_guest_sip_template: Relationship to meeting guest EndpointSIP template.
        country: Two character country code.

    """

    __tablename__: str = "tenant"
    __table_args__: tuple = (
        Index("tenant__idx__global_sip_template_uuid", "global_sip_template_uuid"),
        Index("tenant__idx__webrtc_sip_template_uuid", "webrtc_sip_template_uuid"),
        Index(
            "tenant__idx__registration_trunk_sip_template_uuid",
            "registration_trunk_sip_template_uuid",
        ),
        Index(
            "tenant__idx__meeting_guest_sip_template_uuid",
            "meeting_guest_sip_template_uuid",
        ),
        Index(
            "tenant__idx__twilio_trunk_sip_template_uuid",
            "twilio_trunk_sip_template_uuid",
        ),
    )

    uuid: Mapped[str] = mapped_column(
        String(36), server_default=func.uuid_generate_v4(), primary_key=True
    )
    slug: Mapped[str | None] = mapped_column(String(10), nullable=True)
    sip_templates_generated: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    global_sip_template_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "endpoint_sip.uuid",
            ondelete="SET NULL",
            # NOTE: FK must be named to avoid circular deps on DROP
            name="tenant_global_sip_template_uuid_fkey",
        ),
        nullable=True,
    )
    webrtc_sip_template_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "endpoint_sip.uuid",
            ondelete="SET NULL",
            # NOTE: FK must be named to avoid circular deps on DROP
            name="tenant_webrtc_sip_template_uuid_fkey",
        ),
        nullable=True,
    )
    registration_trunk_sip_template_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "endpoint_sip.uuid",
            ondelete="SET NULL",
            # NOTE: FK must be named to avoid circular deps on DROP
            name="tenant_registration_trunk_sip_template_uuid_fkey",
        ),
        nullable=True,
    )
    meeting_guest_sip_template_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "endpoint_sip.uuid",
            ondelete="SET NULL",
            # NOTE: FK must be named to avoid circular deps on DROP
            name="tenant_meeting_guest_sip_template_uuid_fkey",
        ),
        nullable=True,
    )

    twilio_trunk_sip_template_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "endpoint_sip.uuid",
            ondelete="SET NULL",
            # NOTE: FK must be named to avoid circular deps on DROP
            name="tenant_twilio_trunk_sip_template_uuid_fkey",
        ),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    # Two character country code.

    global_sip_template: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP",
        uselist=False,
        primaryjoin="EndpointSIP.uuid == Tenant.global_sip_template_uuid",
        viewonly=True,
    )
    webrtc_sip_template: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP",
        uselist=False,
        primaryjoin="EndpointSIP.uuid == Tenant.webrtc_sip_template_uuid",
        viewonly=True,
    )  # Relationship to the WebRTC EndpointSIP template.

    registration_trunk_sip_template: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP",
        uselist=False,
        primaryjoin="EndpointSIP.uuid == Tenant.registration_trunk_sip_template_uuid",
        viewonly=True,
    )  # Relationship to registration trunk EndpointSIP template.

    meeting_guest_sip_template: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP",
        uselist=False,
        primaryjoin="EndpointSIP.uuid == Tenant.meeting_guest_sip_template_uuid",
        viewonly=True,
    )  # Relationship to meeting guest EndpointSIP template.

    twilio_trunk_sip_template: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP",
        uselist=False,
        primaryjoin="EndpointSIP.uuid == Tenant.twilio_trunk_sip_template_uuid",
        viewonly=True,
    )
