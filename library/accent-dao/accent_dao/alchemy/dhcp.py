# file: accent_dao/models/dhcp.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class Dhcp(Base):
    """Represents DHCP settings.

    Attributes:
        id: The unique identifier for the DHCP settings.
        active: Indicates if DHCP is active.
        pool_start: The starting IP address of the DHCP pool.
        pool_end: The ending IP address of the DHCP pool.
        network_interfaces: The network interfaces for DHCP.

    """

    __tablename__: str = "dhcp"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    active: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Use integer representation
    pool_start: Mapped[str] = mapped_column(
        String(64), nullable=False, server_default=""
    )
    pool_end: Mapped[str] = mapped_column(String(64), nullable=False, server_default="")
    network_interfaces: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=""
    )
