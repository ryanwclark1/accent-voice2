# file: accent_dao/alchemy/user_external_app.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class UserExternalApp(Base):
    """Represents an external application associated with a user.

    Attributes:
        name: The name of the external application.
        user_uuid: The UUID of the associated user.
        label: A label for the external application.
        configuration: Configuration data for the application (as JSON).

    """

    __tablename__: str = "user_external_app"

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    user_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("userfeatures.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    label: Mapped[str | None] = mapped_column(Text, nullable=True)
    configuration: Mapped[dict | None] = mapped_column(
        JSONB(none_as_null=True), nullable=True
    )
