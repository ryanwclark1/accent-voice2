# file: accent_dao/models/infos.py
# Copyright 2025 Accent Communications

from sqlalchemy import Boolean, String, func
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.uuid import new_uuid


class Infos(Base):
    """Represents system information.

    Attributes:
        uuid: The unique identifier for the information.
        accent_version: The version of the Accent system.
        live_reload_enabled: Indicates if live reload is enabled.
        timezone: The system timezone.
        configured: Indicates if the system is configured.

    """

    __tablename__: str = "infos"

    uuid: Mapped[str] = mapped_column(
        String(38), nullable=False, default=new_uuid, primary_key=True
    )
    accent_version: Mapped[str] = mapped_column(String(64), nullable=False)
    live_reload_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )  # Keep server default
    timezone: Mapped[str | None] = mapped_column(String(128), nullable=True)
    configured: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.false()
    )  # Keep server default
