# file: accent_dao/alchemy/stat_agent.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import Boolean, Index, Integer, PrimaryKeyConstraint, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import case
from sqlalchemy.sql.expression import ColumnElement

from accent_dao.helpers.db_manager import Base


class StatAgent(Base):
    """Represents statistics for an agent.

    Attributes:
        id: The unique identifier for the agent statistics.
        name: The name of the agent.
        tenant_uuid: The UUID of the tenant the agent belongs to.
        agent_id: The ID of the associated agent.
        deleted: Indicates if the agent statistics entry is deleted.
        number: The agent's number (derived from the name).

    """

    __tablename__: str = "stat_agent"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        Index("stat_agent__idx_name", "name"),
        Index("stat_agent__idx_tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    tenant_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    agent_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )  # keep

    @property
    def number(self) -> str | None:
        """The agent's number (extracted from the name)."""
        if self.name.startswith("Agent/"):
            return self.name.split("/")[-1]
        return None

    @number.expression  # type: ignore[no-redef]
    def number(cls) -> ColumnElement[str | None]:
        """Extract and return the substring of `cls.name` starting from the 7th char.

        If the first 6 characters of `cls.name` match "Agent/", return the substring.
        If the condition is not met, return None.

        Returns:
            Mapped[str | None]: The extracted substring or None.

        """
        return func.coalesce(
            case(
                (func.substr(cls.name, 0, 7) == "Agent/", func.substr(cls.name, 7)),
                else_=None,
            ),
            None,
        )
