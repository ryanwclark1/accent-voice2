# accent_auth/policies/models.py

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
    func,
    Index,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from accent_auth.db.base import Base


class Policy(Base):
    __tablename__ = "auth_policy"
    __table_args__ = (
        UniqueConstraint("name", "tenant_uuid", name="auth_policy_name_tenant"),
        Index(
            "auth_policy__idx__slug", func.lower("slug"), "tenant_uuid", unique=True
        ),  # Corrected
        Index("auth_policy__idx__tenant_uuid", "tenant_uuid"),  # Add this line
        {"schema": "auth"},
    )

    uuid: Mapped[str] = mapped_column(
        String(38), server_default=text("gen_random_uuid()"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    tenant_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    config_managed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=True
    )
    shared: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    tenant: Mapped["Tenant"] = relationship(  # Add this relationship
        "Tenant",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
    )
    accesses: Mapped[list["Access"]] = relationship(
        "Access", secondary="auth_policy_access", viewonly=True
    )
    groups: Mapped[list["Group"]] = relationship(
        "Group", secondary="auth_group_policy", viewonly=True
    )

    @property
    def acl(self):
        return [access.access for access in self.accesses]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tenant_uuid_exposed = None
        self.read_only = None
        self.shared_exposed = None


class Access(Base):
    __tablename__ = "auth_access"
    __table_args__ = (
        UniqueConstraint("access"),
        {"schema": "auth"},
    )
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    access: Mapped[str] = mapped_column(Text, nullable=False)


class PolicyAccess(Base):
    __tablename__ = "auth_policy_access"
    __table_args__ = ({"schema": "auth"},)

    policy_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_policy.uuid", ondelete="CASCADE"), primary_key=True
    )
    access_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("auth_access.id", ondelete="CASCADE"), primary_key=True
    )


from accent_auth.tenants.models import Tenant
from accent_auth.groups.models import Group
