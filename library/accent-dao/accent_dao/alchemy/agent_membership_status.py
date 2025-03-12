# file: accent_dao/models/agent_membership_status.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class AgentMembershipStatus(Base):
    """Represents the membership status of an agent in a queue.

    Attributes:
        agent_id: The unique identifier of the agent.
        queue_id: The unique identifier of the queue.
        queue_name: The name of the queue.
        penalty: The penalty associated with the agent's membership.

    """

    __tablename__: str = "agent_membership_status"
    __table_args__: tuple = (
        PrimaryKeyConstraint("agent_id", "queue_id"),
        Index("agent_membership_status__idx__agent_id", "agent_id"),
        Index("agent_membership_status__idx__queue_id", "queue_id"),
    )

    agent_id: Mapped[int] = mapped_column(
        Integer, autoincrement=False, primary_key=True
    )
    queue_id: Mapped[int] = mapped_column(
        Integer, autoincrement=False, primary_key=True
    )
    queue_name: Mapped[str] = mapped_column(String(128), nullable=False)
    penalty: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
