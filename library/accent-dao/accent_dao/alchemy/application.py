# file: accent_dao/alchemy/application.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .application_dest_node import ApplicationDestNode
    from .dialaction import Dialaction
    from .linefeatures import LineFeatures


class Application(Base):
    """Represents an application.

    Attributes:
        uuid: The unique identifier for the application.
        tenant_uuid: The UUID of the tenant the application belongs to.
        name: The name of the application.
        dest_node: Relationship to the ApplicationDestNode model.
        lines: Relationship to LineFeatures.
        _dialaction_actions: Relationship to Dialaction.

    """

    __tablename__: str = "application"
    __table_args__: tuple = (Index("application__idx__tenant_uuid", "tenant_uuid"),)

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)

    dest_node: Mapped["ApplicationDestNode"] = relationship(
        "ApplicationDestNode",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
    )

    lines: Mapped[list["LineFeatures"]] = relationship("LineFeatures", viewonly=True)

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'application:custom',
            Dialaction.actionarg1 == cast(Application.uuid, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )
