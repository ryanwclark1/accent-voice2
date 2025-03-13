# file: accent_dao/alchemy/sccpdevice.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class SCCPDevice(Base):
    """Represents an SCCP device.

    Attributes:
        id: The unique identifier for the device.
        name: The name of the device.
        device: The device identifier.
        line: The associated line.

    """

    __tablename__: str = "sccpdevice"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    device: Mapped[str] = mapped_column(String(80), nullable=False)
    line: Mapped[str] = mapped_column(String(80), nullable=False, server_default="")
