# file: accent_dao/alchemy/moh.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.uuid import new_uuid


class MOH(Base):
    """Represents Music on Hold (MOH) settings.

    Attributes:
        uuid: The unique identifier for the MOH setting.
        tenant_uuid: The UUID of the tenant the MOH setting belongs to.
        name: The name of the MOH setting.
        label: A label for the MOH setting.
        mode: The mode of the MOH setting.
        application: The application associated with the MOH setting.
        sort: The sorting order.

    """

    __tablename__: str = "moh"
    __table_args__: tuple = (
        UniqueConstraint("name"),
        Index("moh__idx__tenant_uuid", "tenant_uuid"),
    )

    uuid: Mapped[str] = mapped_column(
        String(38), nullable=False, default=new_uuid, primary_key=True
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    mode: Mapped[str] = mapped_column(Text, nullable=False)
    application: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort: Mapped[str | None] = mapped_column(Text, nullable=True)
