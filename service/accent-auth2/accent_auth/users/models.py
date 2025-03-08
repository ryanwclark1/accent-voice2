# accent_auth/users/models.py

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
    Index,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from accent_auth.db.base import Base  # Import Base from the new location


class User(Base):
    """Represents a user."""

    __tablename__ = "auth_user"
    __table_args__ = (
        UniqueConstraint("username", name="auth_user_username_key"),
        {"schema": "auth"},
    )

    uuid: Mapped[str] = mapped_column(
        String(38),
        server_default=text("gen_random_uuid()"),  # Use gen_random_uuid()
        primary_key=True,
    )
    username: Mapped[str | None] = mapped_column(String(256), unique=True)
    firstname: Mapped[str | None] = mapped_column(Text)
    lastname: Mapped[str | None] = mapped_column(Text)
    password_hash: Mapped[str | None] = mapped_column(Text)
    password_salt: Mapped[bytes | None] = mapped_column(LargeBinary)
    purpose: Mapped[str] = mapped_column(
        Text,
        CheckConstraint("purpose in ('user', 'internal', 'external_api')"),
        nullable=False,
    )
    authentication_method: Mapped[str] = mapped_column(
        Text,
        CheckConstraint(
            "authentication_method in ('default', 'native', 'ldap', 'saml')"
        ),
        nullable=False,
    )
    enabled: Mapped[bool | None] = mapped_column(Boolean)
    tenant_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    roles: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )  # Added roles.

    # Relationships (assuming other models are defined similarly)
    emails: Mapped[list["Email"]] = relationship(
        "Email", back_populates="user"
    )  # back_populates
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user"
    )  # Assuming you have a RefreshToken model
    # user_group: Mapped[list["UserGroup"]] = relationship("UserGroup", back_populates="user")  # Assuming you'll have a UserGroup model
    # user_policy: Mapped[list["UserPolicy"]] = relationship("UserPolicy", back_populates="user") # Assuming you'll have a UserPolicy model
    __table_args__ = (
        Index("auth_user__idx__tenant_uuid", "tenant_uuid"),
        {"schema": "auth"},
    )


class Email(Base):
    """Represents an email address associated with a user."""

    __tablename__ = "auth_email"
    __table_args__ = ({"schema": "auth"},)

    uuid: Mapped[str] = mapped_column(
        String(38),
        server_default=text("gen_random_uuid()"),  # Use gen_random_uuid()
        primary_key=True,
    )
    address: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("auth_user.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="emails")


class UserExternalAuth(Base):
    """Represents a user's external authentication data."""

    __tablename__ = "auth_user_external_auth"
    __table_args__ = (
        UniqueConstraint(
            "user_uuid",
            "external_auth_type_uuid",
            name="auth_external_user_type_auth_constraint",
        ),
        {"schema": "auth"},
    )

    user_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("auth_user.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    external_auth_type_uuid: Mapped[str] = mapped_column(
        String(38),
        ForeignKey("auth_externalauthtype.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    data: Mapped[str] = mapped_column(Text, nullable=False)


class UserGroup(Base):
    """Represents the relationship between users and groups."""

    __tablename__ = "auth_user_group"
    __table_args__ = ({"schema": "auth"},)

    group_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_group.uuid", ondelete="CASCADE"), primary_key=True
    )
    user_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_user.uuid", ondelete="CASCADE"), primary_key=True
    )


class UserPolicy(Base):
    """Represents the relationship between users and policies."""

    __tablename__ = "auth_user_policy"
    __table_args__ = ({"schema": "auth"},)

    policy_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_policy.uuid", ondelete="CASCADE"), primary_key=True
    )
    user_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_user.uuid", ondelete="CASCADE"), primary_key=True
    )


from accent_auth.auth.models import (
    Token,
    RefreshToken,
    Session,
)  # Import at the end to prevent circular import issues
from accent_auth.tenants.models import Tenant, Domain, Group, Policy, ExternalAuthType
