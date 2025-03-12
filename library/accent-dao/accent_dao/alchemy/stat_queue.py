# file: accent_dao/models/stat_queue.py
# Copyright 2025 Accent Communications

from sqlalchemy import Boolean, Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class StatQueue(Base):
    """Represents statistics for a queue.

    Attributes:
        id: The unique identifier for the queue statistics.
        name: The name of the queue.
        tenant_uuid: The UUID of the tenant the queue belongs to.
        queue_id: The ID of the associated queue.
        deleted: Indicates if the queue statistics entry is deleted.

    """

    __tablename__: str = "stat_queue"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        Index("stat_queue__idx_name", "name"),
        Index("stat_queue__idx_tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    tenant_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    queue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )  # Keep server default
