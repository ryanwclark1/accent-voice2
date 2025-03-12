# file: accent_dao/models/feature_extension.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent.accent_helpers import clean_extension
from sqlalchemy import Boolean, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class FeatureExtension(Base):
    """Represents a feature extension.

    Attributes:
        uuid: The unique identifier for the feature extension.
        enabled: Indicates if the feature extension is enabled.
        exten: The extension number.
        feature: The feature associated with the extension.

    """

    __tablename__: str = "feature_extension"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )
    exten: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    feature: Mapped[str] = mapped_column(String(255), nullable=False)

    def is_pattern(self) -> bool:
        """Check if extension pattern starts underscore."""
        return self.exten.startswith("_")

    def clean_exten(self) -> str:
        """Clean the extension number."""
        return clean_extension(self.exten)
