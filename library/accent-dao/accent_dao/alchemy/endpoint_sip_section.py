# file: accent_dao/models/endpoint_sip_section.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Enum, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
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

    __mapper_args__: dict[str, str | Mapped] = {  # type: ignore
        "polymorphic_on": type,
        "polymorphic_identity": "section",
    }

    _options: Mapped[list["EndpointSIPSectionOption"]] = relationship(
        "EndpointSIPSectionOption",
        cascade="all, delete-orphan",
        passive_deletes=True,
        # Removed lazy loading
    )

    @property
    def options(self) -> list[list[str]]:
        """A list of key-value pairs representing the section options."""
        return [[option.key, option.value] for option in self._options]

    @options.setter
    def options(self, options: list[list[str]]) -> None:
        """Set the section options

        Args:
            options: New options to be set.

        Returns:
            None

        """
        # Build dictionaries for existing and new options for easy lookup.
        existing_options = {option.key: option for option in self._options}
        new_options = {key: value for key, value in options}

        # Update existing options and add new ones.
        updated_options = []
        for key, value in new_options.items():
            if key in existing_options:
                # Update existing option
                existing_options[key].value = value
                updated_options.append(existing_options[key])
            else:
                # Add new option.  Create a new EndpointSIPSectionOption.
                updated_options.append(EndpointSIPSectionOption(key=key, value=value))

        # Set the updated options list, which automatically handles deletions
        # due to the cascade configuration.
        self._options = updated_options

    def find(self, term: str) -> list[tuple[str, str]]:
        """Finds options matching a given term."""
        return [
            (option.key, option.value) for option in self._options if option.key == term
        ]

    def add_or_replace(self, option_name: str, value: str) -> None:
        """Adds a new option or replaces an existing one."""
        for option in self._options:
            if option.key == option_name:
                option.value = value
                return

        self._options.append(EndpointSIPSectionOption(key=option_name, value=value))


class AORSection(EndpointSIPSection):
    """Represents an AOR (Address of Record) section."""

    __mapper_args__: dict[str, str] = {"polymorphic_identity": "aor"}


class AuthSection(EndpointSIPSection):
    """Represents an authentication section."""

    __mapper_args__: dict[str, str] = {"polymorphic_identity": "auth"}


class EndpointSection(EndpointSIPSection):
    """Represents an endpoint section."""

    __mapper_args__: dict[str, str] = {"polymorphic_identity": "endpoint"}


class IdentifySection(EndpointSIPSection):
    """Represents an identify section."""

    __mapper_args__: dict[str, str] = {"polymorphic_identity": "identify"}


class OutboundAuthSection(EndpointSIPSection):
    """Represents an outbound authentication section."""

    __mapper_args__: dict[str, str] = {"polymorphic_identity": "outbound_auth"}


class RegistrationOutboundAuthSection(EndpointSIPSection):
    """Represents a registration outbound authentication section."""

    __mapper_args__: dict[str, str] = {
        "polymorphic_identity": "registration_outbound_auth"
    }


class RegistrationSection(EndpointSIPSection):
    """Represents a registration section."""

    __mapper_args__: dict[str, str] = {"polymorphic_identity": "registration"}
