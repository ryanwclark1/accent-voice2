# file: accent_dao/models/sccpgeneralsettings.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class SCCPGeneralSettings(Base):
    """Represents general settings for SCCP.

    Attributes:
        id: The unique identifier for the setting.
        option_name: The name of the option.
        option_value: The value of the option.

    """

    __tablename__: str = "sccpgeneralsettings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    option_name: Mapped[str] = mapped_column(String(80), nullable=False)
    option_value: Mapped[str] = mapped_column(String(80), nullable=False)
