# file: accent_dao/alchemy/stat_queue.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""StatQueue model definition for queue statistics tracking."""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base


class StatQueue(Base):
    """Represents a queue statistics entity.

    Attributes:
        id: The unique identifier for the statistics queue.
        name: The name of the queue.
        tenant_uuid: The UUID of the tenant this queue belongs to.
        queue_id: The ID of the queue in the ConFD system.
        deleted: Flag indicating if the queue has been deleted.
        periodic_stats: Relationship to periodic statistics for this queue.

    """

    __tablename__: str = "stat_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    tenant_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    queue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    periodic_stats = relationship("StatQueuePeriodic", back_populates="stat_queue")
