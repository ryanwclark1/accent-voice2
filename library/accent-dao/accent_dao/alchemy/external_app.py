# file: accent_dao/models/external_app.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class ExternalApp(Base):
    """Represents an external application.

    Attributes:
        name: The name of the external application.
        tenant_uuid: The UUID of the tenant the application belongs to.
        label: A label for the application.
        configuration: Configuration data for the application (as JSON).

    """

    __tablename__: str = "external_app"

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    label: Mapped[str | None] = mapped_column(Text, nullable=True)
    configuration: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
