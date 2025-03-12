# file: accent_dao/models/mail.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class Mail(Base):
    """Represents mail settings.

    Attributes:
        id: The unique identifier for the mail settings.
        mydomain: The domain name.
        origin: The origin.
        relayhost: The relay host.
        fallback_relayhost: The fallback relay host.
        canonical: Canonical settings.

    """

    __tablename__: str = "mail"

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    mydomain: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default="0"
    )  # Keep server default
    origin: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default="accent-clients.accentvoice.io",
        unique=True,
    )  # Keep server default
    relayhost: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fallback_relayhost: Mapped[str | None] = mapped_column(String(255), nullable=True)
    canonical: Mapped[str] = mapped_column(Text, nullable=False)
