# accent_auth/tenants/models.py

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
    Index,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from accent_auth.db.base import Base  # Import Base from the new location
from accent_auth.database.datatypes import XMLPostgresqlType

RFC_DN_MAX_LENGTH = 253


class Address(Base):
    """Represents an address."""

    __tablename__ = "auth_address"
    __table_args__ = ({"schema": "auth"},)

    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("auth_tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    line_1: Mapped[str | None] = mapped_column(Text)
    line_2: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    state: Mapped[str | None] = mapped_column(Text)
    zip_code: Mapped[str | None] = mapped_column(Text)
    country: Mapped[str | None] = mapped_column(Text)

    # No back_populates to Tenant, one-to-one relationship managed by Tenant


class Tenant(Base):
    __tablename__ = "auth_tenant"
    __table_args__ = ({"schema": "auth"},)
    uuid: Mapped[str] = mapped_column(
        String(38), server_default=text("gen_random_uuid()"), primary_key=True
    )  # No more server_default
    name: Mapped[str | None] = mapped_column(Text, unique=False, nullable=True)
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str | None] = mapped_column(Text)
    contact_uuid: Mapped[str | None] = mapped_column(
        String(38), ForeignKey("auth_user.uuid", ondelete="SET NULL")
    )
    parent_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("auth_tenant.uuid"),
        nullable=False,
    )
    default_authentication_method: Mapped[str] = mapped_column(
        Text,
        CheckConstraint("default_authentication_method in ('native', 'ldap', 'saml')"),
        nullable=False,
    )

    domains: Mapped[list["Domain"]] = relationship(
        "Domain",
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="tenant",
    )
    address: Mapped["Address"] = relationship(
        "Address",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @hybrid_property
    def domain_names(self):
        if self.domains:
            return [domain.name for domain in self.domains]
        else:
            return []

    @domain_names.setter
    def domain_names(self, value):
        current_names = {domain.name for domain in self.domains}
        new_names = set(value)
        missing_names = new_names - current_names
        domains = set()

        for domain in self.domains:
            if domain.name in new_names:
                domains.add(domain)

        for name in missing_names:
            domains.add(Domain(name=name, tenant=self))

        self.domains = list(domains)


class Domain(Base):
    __tablename__ = "auth_tenant_domain"
    __table_args__ = ({"schema": "auth"},)
    uuid: Mapped[str] = mapped_column(
        String(36),
        server_default=text("gen_random_uuid()"),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(RFC_DN_MAX_LENGTH), nullable=False, unique=True
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="domains")


class Group(Base):
    """Represents a group."""

    __tablename__ = "auth_group"
    __table_args__ = ({"schema": "auth"},)
    uuid: Mapped[str] = mapped_column(
        String(38),
        server_default=text("gen_random_uuid()"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    tenant_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    system_managed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    __table_args__ = (
        UniqueConstraint("name", "tenant_uuid", name="auth_group_name_tenant"),
        Index("auth_group__idx__slug", func.lower(slug), "tenant_uuid", unique=True),
        Index("auth_group__idx__tenant_uuid", "tenant_uuid"),
    )
    policies: Mapped[List["Policy"]] = relationship(
        secondary="auth_group_policy", back_populates="groups"
    )


class GroupPolicy(Base):
    """Represents the relationship between groups and policies."""

    __tablename__ = "auth_group_policy"
    __table_args__ = ({"schema": "auth"},)

    policy_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_policy.uuid", ondelete="CASCADE"), primary_key=True
    )
    group_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_group.uuid", ondelete="CASCADE"), primary_key=True
    )


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
        Boolean, default=False, server_default="false", nullable=False
    )
    shared: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    tenant: Mapped["Tenant"] = relationship(
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


class ExternalAuthType(Base):
    """Represents a type of external authentication."""

    __tablename__ = "auth_external_auth_type"
    __table_args__ = ({"schema": "auth"},)
    uuid: Mapped[str] = mapped_column(
        String(38),
        server_default=text("gen_random_uuid()"),  # Use gen_random_uuid()
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, server_default="false")


class ExternalAuthConfig(Base):
    """Represents the configuration for an external authentication type."""

    __tablename__ = "auth_external_auth_config"
    __table_args__ = ({"schema": "auth"},)
    tenant_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_tenant.uuid", ondelete="CASCADE"), primary_key=True
    )
    type_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("auth_externalauthtype.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    data: Mapped[str] = mapped_column(Text, nullable=False)


class LDAPConfig(Base):
    __tablename__ = "auth_ldap_config"
    __table_args__ = ({"schema": "auth"},)
    tenant_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("auth_tenant.uuid", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    host: Mapped[str] = mapped_column(String(512), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    protocol_version: Mapped[int] = mapped_column(SmallInteger)
    protocol_security: Mapped[str | None] = mapped_column(
        Text,
        CheckConstraint("protocol_security in ('ldaps', 'tls')"),
    )
    bind_dn: Mapped[str | None] = mapped_column(String(256))
    bind_password: Mapped[str | None] = mapped_column(Text)
    user_base_dn: Mapped[str] = mapped_column(String(256), nullable=False)
    user_login_attribute: Mapped[str] = mapped_column(String(64), nullable=False)
    user_email_attribute: Mapped[str] = mapped_column(String(64), nullable=False)
    search_filters: Mapped[str | None] = mapped_column(Text, nullable=True)


class SAMLConfig(Base):
    __tablename__ = "auth_saml_config"
    __table_args__ = ({"schema": "auth"},)

    tenant_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("auth_tenant.uuid", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    domain_uuid: Mapped[str] = mapped_column(
        String(length=38),
        ForeignKey("auth_tenant_domain.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    entity_id: Mapped[str] = mapped_column(String(512), nullable=False)
    idp_metadata: Mapped[str] = mapped_column(XMLPostgresqlType(), nullable=False)
    acs_url: Mapped[str] = mapped_column(String(512), nullable=False)


class SAMLSession(Base):
    __tablename__ = "auth_saml_session"
    __table_args__ = ({"schema": "auth"},)
    request_id: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        primary_key=True,
    )
    session_id: Mapped[str] = mapped_column(
        String(length=22),
        nullable=False,
        primary_key=True,
    )
    redirect_url: Mapped[str] = mapped_column(String(512), nullable=False)
    domain: Mapped[str] = mapped_column(String(512), nullable=False)
    relay_state: Mapped[str] = mapped_column(String(100), nullable=False)
    login: Mapped[str | None] = mapped_column(String(512), nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    saml_name_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    refresh_token_uuid: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("auth_refresh_token.uuid", ondelete="SET NULL"),
        nullable=True,
    )


class SAMLPysaml2Cache(Base):
    __tablename__ = "auth_saml_pysaml2_cache"
    __table_args__ = ({"schema": "auth"},)
    name_id: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        primary_key=True,
    )
    entity_id: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
        primary_key=True,
    )
    info: Mapped[str] = mapped_column(Text(), nullable=False)
    not_on_or_after: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )


# Circular import resolution
from accent_auth.auth.models import Token, RefreshToken, Session
from accent_auth.users.models import (
    User,
    Email,
    UserExternalAuth,
    UserGroup,
    UserPolicy,
)
