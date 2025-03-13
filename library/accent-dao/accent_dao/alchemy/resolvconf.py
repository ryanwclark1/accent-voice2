# file: accent_dao/alchemy/resolvconf.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class Resolvconf(Base):
    """Represents DNS resolver configuration.

    Attributes:
        id: The unique identifier for the configuration entry.
        hostname: The hostname.
        domain: The domain name.
        nameserver1: The primary nameserver.
        nameserver2: The secondary nameserver.
        nameserver3: The tertiary nameserver.
        search: The search domain list.
        description: A description of the configuration.

    """

    __tablename__: str = "resolvconf"
    __table_args__: tuple = (UniqueConstraint("domain"),)

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    hostname: Mapped[str] = mapped_column(
        String(63), nullable=False, server_default="accent"
    )  # Keep server default
    domain: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=""
    )  # Keep server default
    nameserver1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nameserver2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nameserver3: Mapped[str | None] = mapped_column(String(255), nullable=True)
    search: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
