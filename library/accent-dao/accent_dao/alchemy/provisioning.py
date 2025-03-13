# file: accent_dao/alchemy/provisioning.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class Provisioning(Base):
    """Represents provisioning settings.

    Attributes:
        id: The unique identifier for the provisioning settings.
        net4_ip: The IPv4 network address.
        http_base_url: The base URL for HTTP provisioning.
        dhcp_integration: Indicates if DHCP integration is enabled.
        http_port: The HTTP port for provisioning.

    """

    __tablename__: str = "provisioning"

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    net4_ip: Mapped[str | None] = mapped_column(String(39), nullable=True)
    http_base_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dhcp_integration: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    http_port: Mapped[int] = mapped_column(Integer, nullable=False)
