# file: accent_dao/models/pjsip_transport_option.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, Index, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class PJSIPTransportOption(Base):
    """Represents an option for a PJSIP transport.

    Attributes:
        id: The unique identifier for the option.
        key: The name of the option.
        value: The value of the option.
        pjsip_transport_uuid: The UUID of the associated PJSIP transport.
        option: A computed property representing the key-value pair.

    """

    __tablename__: str = "pjsip_transport_option"
    __table_args__: tuple = (
        Index(
            "pjsip_transport_option__idx__pjsip_transport_uuid",
            "pjsip_transport_uuid",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )  # No longer autoincrement
    key: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    pjsip_transport_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pjsip_transport.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    @property
    def option(self) -> list[str]:
        """A list containing the key and value of the option."""
        return [self.key, self.value]

    @option.setter
    def option(self, option: list[str]) -> None:
        """Set the key and value of the option."""
        self.key, self.value = option
