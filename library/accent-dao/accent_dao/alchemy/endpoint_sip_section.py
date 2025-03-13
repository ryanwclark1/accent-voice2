# file: accent_dao/alchemy/endpoint_sip_section.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import Any, Literal

from sqlalchemy import Enum, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

from .endpoint_sip_section_option import EndpointSIPSectionOption

EndpointSipSectionType = Literal[
    "aor",
    "auth",
    "endpoint",
    "identify",
    "outbound_auth",
    "registration_outbound_auth",
    "registration",
]


class EndpointSIPSection(Base):
    """Represents a section within a SIP endpoint configuration.

    Attributes:
        uuid: The unique identifier for the section.
        type: The type of the section.
        endpoint_sip_uuid: The UUID of the associated SIP endpoint.
        _options: Relationship to EndpointSIPSectionOption.
        options: A list of key-value pairs representing the section options.

    """

    __tablename__: str = "endpoint_sip_section"
    __table_args__: tuple = (
        UniqueConstraint("type", "endpoint_sip_uuid"),
        Index("endpoint_sip_section__idx__endpoint_sip_uuid", "endpoint_sip_uuid"),
    )

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
    )
    type: Mapped[EndpointSipSectionType] = mapped_column(
        Enum(
            "aor",
            "auth",
            "endpoint",
            "identify",
            "outbound_auth",
            "registration_outbound_auth",
            "registration",
            name="endpoint_sip_section_type",
        ),
        nullable=False,
    )
    endpoint_sip_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoint_sip.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    __mapper_args__: dict[str, str | Mapped[Any]] = {
        "polymorphic_on": type,
        "polymorphic_identity": "section",
    }

    _options: Mapped[list["EndpointSIPSectionOption"]] = relationship(
        "EndpointSIPSectionOption",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    options = association_proxy(
        "_options",
        "option",
        creator=lambda key, value: EndpointSIPSectionOption(key=key, value=value),
    )

    def find(self, term: str) -> list[tuple[str, str]]:
        """Find options matching a given term."""
        return [
            (option.key, option.value) for option in self._options if option.key == term
        ]

    def add_or_replace(self, option_name: str, value: str) -> None:
        """Add a new option or replaces an existing one."""
        for option in self._options:
            if option.key == option_name:
                option.value = value
                return

        self._options.append(EndpointSIPSectionOption(key=option_name, value=value))


class AORSection(EndpointSIPSection):
    """Represents an AOR (Address of Record) section."""

    __mapper_args__: dict[str, str | Mapped[Any]] = {"polymorphic_identity": "aor"}


class AuthSection(EndpointSIPSection):
    """Represents an authentication section."""

    __mapper_args__: dict[str, str | Mapped[Any]] = {
        "polymorphic_identity": "auth"
    }


class EndpointSection(EndpointSIPSection):
    """Represents an endpoint section."""

    __mapper_args__: dict[str, str | Mapped[Any]] = {
        "polymorphic_identity": "endpoint"
    }


class IdentifySection(EndpointSIPSection):
    """Represents an identify section."""

    __mapper_args__: dict[str, str | Mapped[Any]] = {
        "polymorphic_identity": "identify"
    }


class OutboundAuthSection(EndpointSIPSection):
    """Represents an outbound authentication section."""

    __mapper_args__: dict[str, str | Mapped[Any]] = {
        "polymorphic_identity": "outbound_auth"
    }


class RegistrationOutboundAuthSection(EndpointSIPSection):
    """Represents a registration outbound authentication section."""

    __mapper_args__: dict[str, str | Mapped[Any]] = {
        "polymorphic_identity": "registration_outbound_auth"
    }


class RegistrationSection(EndpointSIPSection):
    """Represents a registration section."""

    __mapper_args__: dict[str, str | Mapped[Any]] = {
        "polymorphic_identity": "registration"
    }
