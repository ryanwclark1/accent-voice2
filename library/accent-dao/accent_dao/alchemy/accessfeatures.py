# file: accent_dao/models/accessfeatures.py
# Copyright 2025 Accent Communications

from sqlalchemy import CheckConstraint, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class AccessFeatures(Base):
    """Represents access features in the database.

    Attributes:
        id: The unique identifier for the access feature.
        host: The host associated with the feature.
        commented: A flag indicating whether the feature is commented out.
        feature: The name of the feature (constrained to 'phonebook').
        enabled: A computed property indicating if the feature is enabled.

    """

    __tablename__: str = "accessfeatures"
    __table_args__: tuple = (
        CheckConstraint("feature='phonebook'"),
        UniqueConstraint("host", "feature"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    commented: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Use Integer, not boolean
    feature: Mapped[str] = mapped_column(
        String(64), nullable=False, server_default="phonebook"
    )

    @property
    def enabled(self) -> bool:
        """Indicates whether the feature is enabled.

        A feature is considered enabled if it is not commented out.
        """
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set the enabled/disabled status by adjusting the comment.

        Args:
            value: Boolean value to set.

        """
        self.commented = int(not value)  # 0 if True, 1 if False
