# file: accent_dao/alchemy/phone_number.py
# Copyright 2025 Accent Communications

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, text

from accent_dao.helpers.db_manager import Base


class PhoneNumber(Base):
    """Represents a phone number.

    Attributes:
        uuid: The unique identifier for the phone number.
        tenant_uuid: The UUID of the tenant the phone number belongs to.
        number: The phone number.
        caller_id_name: The caller ID name associated with the number.
        shared: Indicates if the phone number is shared.
        _main: Internal flag to indicate if this is the main number for the tenant.
        main: Indicates if the phone number is the main number for the tenant.

    """

    __tablename__: str = "phone_number"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ("tenant_uuid",),
            ("tenant.uuid",),
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "CASE WHEN main THEN shared ELSE true END",
            name="phone_number_shared_if_main",
        ),
    )

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4(), primary_key=True
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), nullable=False, index=True, unique=False
    )  # Removed unique constraint here.
    number: Mapped[str] = mapped_column(
        Text, nullable=False, unique=True
    )  # Keep unique constraint here
    caller_id_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    shared: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.false()
    )
    _main: Mapped[bool] = mapped_column(
        "main", Boolean, nullable=False, server_default=func.false()
    )
    # Added Index for only one main number allowed.
    __table_args__ = (
        Index(
            "only_one_main_allowed",
            "main",
            "tenant_uuid",
            unique=True,
            postgresql_where=(text("main is true")),
        ),
    )

    @property
    def main(self) -> bool:
        """Indicate if the phone number is the main number for the tenant."""
        return self._main

    @main.setter
    def main(self, value: bool) -> None:
        """Set whether the phone number is the main number."""
        self._main = value
        if value:
            self.shared = True

    def __repr__(self) -> str:
        """Return a string representation of the phone number."""
        return f"{self.__class__.__name__}(uuid={self.uuid}, number={self.number})"
