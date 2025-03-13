# file: accent_dao/alchemy/agentfeatures.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .agentqueueskill import AgentQueueSkill
    from .func_key_dest_agent import FuncKeyDestAgent
    from .queuemember import QueueMember
    from .userfeatures import UserFeatures


class AgentFeatures(Base):
    """Represents agent features.

    Attributes:
        id: The unique identifier for the agent.
        tenant_uuid: The UUID of the tenant the agent belongs to.
        firstname: The first name of the agent.
        lastname: The last name of the agent.
        number: The agent's number.
        passwd: The agent's password.
        context: The context associated with the agent.
        language: The agent's preferred language.
        autologoff: The autologoff time for the agent (in seconds).
        group: The group the agent belongs to.
        description: A description of the agent.
        preprocess_subroutine:  A preprocess subroutine.
        func_keys: Relationship to the FuncKeyDestAgent model.
        queue_queue_members: Relationship to the QueueMember model.
        agent_queue_skills: Relationship to the AgentQueueSkill model.
        users: Relationship to UserFeatures model.

    """

    __tablename__: str = "agentfeatures"
    __table_args__: tuple = (
        UniqueConstraint("number", "tenant_uuid"),
        Index("agentfeatures__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    firstname: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lastname: Mapped[str | None] = mapped_column(String(128), nullable=True)
    number: Mapped[str] = mapped_column(String(40), nullable=False)
    passwd: Mapped[str | None] = mapped_column(String(128), nullable=True)
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    autologoff: Mapped[int | None] = mapped_column(Integer, nullable=True)
    group: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    preprocess_subroutine: Mapped[str | None] = mapped_column(String(79), nullable=True)

    func_keys: Mapped[list["FuncKeyDestAgent"]] = relationship(
        "FuncKeyDestAgent", cascade="all, delete-orphan"
    )

    queue_queue_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'queue',
            QueueMember.usertype == 'agent',
            QueueMember.userid == AgentFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
        cascade="all, delete-orphan",
    )

    agent_queue_skills: Mapped[list["AgentQueueSkill"]] = relationship(
        "AgentQueueSkill",
        primaryjoin="AgentQueueSkill.agentid == AgentFeatures.id",
        foreign_keys="AgentQueueSkill.agentid",
        cascade="all, delete-orphan",
    )

    users: Mapped[list["UserFeatures"]] = relationship(
        "UserFeatures",
        primaryjoin="AgentFeatures.id == UserFeatures.agentid",
        foreign_keys="UserFeatures.agentid",
        viewonly=True,
    )
