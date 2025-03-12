# file: accent_dao/models/agent_login_status.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .agentfeatures import AgentFeatures


class AgentLoginStatus(Base):
    """Represents the login status of an agent.

    Attributes:
        agent_id: The unique identifier of the agent.
        agent_number: The agent's number.
        extension: The extension associated with the agent.
        context: The context associated with the agent.
        interface: The interface the agent is logged in on.
        state_interface: The state interface of the agent.
        paused: Indicates if the agent is paused.
        paused_reason: The reason for the agent being paused (if applicable).
        login_at: The timestamp when the agent logged in.
        agent: Relationship to the AgentFeatures model.

    """

    __tablename__: str = "agent_login_status"
    __table_args__: tuple = (
        PrimaryKeyConstraint("agent_id"),
        UniqueConstraint("extension", "context"),
        UniqueConstraint("interface"),
        Index("agent_login_status__idx__agent_id", "agent_id"),
    )

    agent_id: Mapped[int] = mapped_column(
        Integer, autoincrement=False, primary_key=True
    )
    agent_number: Mapped[str] = mapped_column(String(40), nullable=False)
    extension: Mapped[str] = mapped_column(String(80), nullable=False)
    context: Mapped[str] = mapped_column(String(79), nullable=False)
    interface: Mapped[str] = mapped_column(String(128), nullable=False)
    state_interface: Mapped[str] = mapped_column(String(128), nullable=False)
    paused: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    paused_reason: Mapped[str | None] = mapped_column(String(80), nullable=True)
    login_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.timezone("utc", func.current_timestamp()),
    )

    agent: Mapped["AgentFeatures"] = relationship(
        "AgentFeatures",
        primaryjoin="AgentLoginStatus.agent_id == AgentFeatures.id",
        foreign_keys="AgentFeatures.id",
        uselist=False,
    )
