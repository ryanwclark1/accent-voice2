# file: accent_dao/models/pjsip_transport.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

from .pjsip_transport_option import PJSIPTransportOption

if TYPE_CHECKING:
    pass


class PJSIPTransport(Base):
    """Represents a PJSIP transport configuration.

    Attributes:
        uuid: The unique identifier for the transport.
        name: The name of the transport.
        _options: Relationship to PJSIPTransportOption (internal use).
        options: A list of key-value pairs representing the transport options.

    """

    __tablename__: str = "pjsip_transport"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4(), primary_key=True
    )
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    _options: Mapped[list["PJSIPTransportOption"]] = relationship(
        "PJSIPTransportOption",
        cascade="all, delete-orphan",
        passive_deletes=True,
        passive_updates=False,
    )

    def __init__(self, options: list[list[str]] | None = None, **kwargs: dict) -> None:
        """Initialize a PJSIPTransport object.

        Args:
            options: A list of key-value pairs representing transport options.
            **kwargs: Additional keyword arguments.

        """
        super().__init__(**kwargs)
        if options:
            for key, value in options:
                self._options.append(PJSIPTransportOption(key=key, value=value))

    @property
    def options(self) -> list[list[str]]:
        """A list of key-value pairs representing the transport options."""
        return [[option.key, option.value] for option in self._options]

    @options.setter
    def options(self, options: list[list[str]]) -> None:
        """Set the transport options.

        Args:
            options: a list of key-value pairs.

        """
        # Build dictionaries of existing and new options for efficient comparison
        existing_options = {option.key: option for option in self._options}
        new_options = {key: value for key, value in options}

        updated_options = []

        # Update existing options or add new ones
        for key, value in new_options.items():
            if key in existing_options:
                existing_options[key].value = value  # Update existing option
                updated_options.append(existing_options[key])
            else:
                # Add new option. Create a new PJSIPTransportOption
                updated_options.append(PJSIPTransportOption(key=key, value=value))

        # Set the _options attribute to the updated list.  SQLAlchemy will
        # automatically handle deleting options that are no longer present.
        self._options = updated_options
