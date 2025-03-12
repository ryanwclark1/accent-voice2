# file: accent_dao/models/queueskillrule.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class QueueSkillRule(Base):
    """Represents a rule for assigning queue skills.

    Attributes:
        id: The unique identifier for the skill rule.
        tenant_uuid: The UUID of the tenant the rule belongs to.
        name: The name of the rule.
        rule: The rule definition (as a string).
        rules: A list of individual rules (derived from the rule string).

    """

    __tablename__: str = "queueskillrule"
    __table_args__: tuple = (Index("queueskillrule__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    rule: Mapped[str | None] = mapped_column(Text, nullable=True)

    @property
    def rules(self) -> list[str]:
        """A list of individual rules (derived from the rule string)."""
        if not self.rule:
            return []
        return self.rule.split(";")

    @rules.expression
    def rules(cls) -> Mapped[list[str] | None]:
        return func.string_to_array(cls.rule, ";")

    @rules.setter
    def rules(self, value: list[str] | None) -> None:
        """Set the rules from a list of strings."""
        self.rule = ";".join(value) if value else None
