# file: accent_dao/alchemy/ingress_http.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class IngressHTTP(Base):
    """Represents an HTTP ingress configuration.

    Attributes:
        uuid: The unique identifier for the HTTP ingress.
        uri: The URI for the ingress.
        tenant_uuid: The UUID of the tenant the ingress belongs to.

    """

    __tablename__: str = "ingress_http"
    __table_args__: tuple = (Index("ingress_http__idx__tenant_uuid", "tenant_uuid"),)

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
    )
    uri: Mapped[str] = mapped_column(Text, nullable=False)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
