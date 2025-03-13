# file: accent_dao/alchemy/endpoint_sip_section_option.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, Index, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class EndpointSIPSectionOption(Base):
    """Represents an option within a SIP endpoint section.

    Attributes:
        uuid: The unique identifier for the option.
        key: The name of the option.
        value: The value of the option.
        endpoint_sip_section_uuid: The UUID of the associated SIP endpoint section.
        option: A computed property representing the key-value pair.

    """

    __tablename__: str = "endpoint_sip_section_option"
    __table_args__: tuple = (
        Index(
            "endpoint_sip_section_option__idx__endpoint_sip_section_uuid",
            "endpoint_sip_section_uuid",
        ),
    )

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4(), primary_key=True
    )
    key: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    endpoint_sip_section_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoint_sip_section.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    @property
    def option(self) -> list[str]:
        """Return a list containing the key and value of the option."""
        return [self.key, self.value]

    @option.setter
    def option(self, option: list[str]) -> None:
        """Set the key and value of the option.

        Args:
            option: A list containing the key and value.

        """
        self.key, self.value = option
