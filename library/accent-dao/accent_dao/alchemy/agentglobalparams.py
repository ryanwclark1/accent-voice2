# file: accent_dao/models/agentglobalparams.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class AgentGlobalParams(Base):
    """Represents global parameters for agents.

    Attributes:
        id: The unique identifier for the parameter.
        category: The category of the parameter.
        option_name: The name of the option.
        option_value: The value of the option.

    """

    __tablename__: str = "agentglobalparams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    option_name: Mapped[str] = mapped_column(String(255), nullable=False)
    option_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
