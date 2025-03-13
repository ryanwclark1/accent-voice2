# file: accent_dao/alchemy/agentqueueskill.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .agentfeatures import AgentFeatures
    from .queueskill import QueueSkill


class AgentQueueSkill(Base):
    """Represents the skill level of an agent for a specific queue.

    Attributes:
        agentid: The ID of the agent.
        skillid: The ID of the skill.
        weight: The weight (priority) of the agent's skill.
        agent: Relationship to the AgentFeatures model.
        skill: Relationship to the QueueSkill model.

    """

    __tablename__: str = "agentqueueskill"
    __table_args__: tuple = (PrimaryKeyConstraint("agentid", "skillid"),)

    agentid: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    skillid: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    weight: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    agent: Mapped["AgentFeatures"] = relationship(
        "AgentFeatures",
        primaryjoin="AgentQueueSkill.agentid == AgentFeatures.id",
        foreign_keys="AgentQueueSkill.agentid",
    )

    skill: Mapped["QueueSkill"] = relationship(
        "QueueSkill",
        primaryjoin="AgentQueueSkill.skillid == QueueSkill.id",
        foreign_keys="AgentQueueSkill.skillid",
    )
