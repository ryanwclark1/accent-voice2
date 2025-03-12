# file: accent_dao/models/queueskill.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .agentqueueskill import AgentQueueSkill


class QueueSkill(Base):
    """Represents a skill for queue members.

    Attributes:
        id: The unique identifier for the skill.
        tenant_uuid: The UUID of the tenant the skill belongs to.
        name: The name of the skill.
        description: A description of the skill.
        agent_queue_skills: Relationship to AgentQueueSkill.
    """

    __tablename__: str = "queueskill"
    __table_args__: tuple = (
        UniqueConstraint("name", "tenant_uuid"),
        Index("queueskill__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(64), server_default="", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    agent_queue_skills: Mapped[list["AgentQueueSkill"]] = relationship(
        "AgentQueueSkill",
        primaryjoin="AgentQueueSkill.skillid == QueueSkill.id",
        foreign_keys="AgentQueueSkill.skillid",
        cascade="all, delete-orphan",
    )
