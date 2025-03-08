# accent_auth/auth/models.py

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    Index,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from accent_auth.db.base import Base


class Token(Base):
    """Represents an authentication token."""

    __tablename__ = "auth_token"
    __table_args__ = (
        Index("auth_token__idx__session_uuid", "session_uuid"),
        {"schema": "auth"},
    )

    uuid: Mapped[str] = mapped_column(
        String(38), server_default=text("gen_random_uuid()"), primary_key=True
    )
    session_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("auth_session.uuid", ondelete="CASCADE"), nullable=False
    )
    auth_id: Mapped[str] = mapped_column(Text, nullable=False)
    pbx_user_uuid: Mapped[str | None] = mapped_column(String(38))
    accent_uuid: Mapped[str | None] = mapped_column(String(38))
    issued_t: Mapped[int | None] = mapped_column(Integer)
    expire_t: Mapped[int | None] = mapped_column(Integer)
    metadata_: Mapped[str | None] = mapped_column("metadata", Text)
    user_agent: Mapped[str | None] = mapped_column(Text, server_default="")
    remote_addr: Mapped[str | None] = mapped_column(Text, server_default="")
    acl: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default="{}"
    )
    refresh_token_uuid: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("auth_refresh_token.uuid", ondelete="SET NULL"),
        nullable=True,
    )

    session: Mapped["Session"] = relationship("Session", passive_deletes=True)


class RefreshToken(Base):
    """Represents a refresh token."""

    __tablename__ = "auth_refresh_token"
    __table_args__ = (
        UniqueConstraint("client_id", "user_uuid", name="uq_client_id_user_uuid"),
        Index("ix_refresh_token_user_uuid", "user_uuid"),  # Add index
        {"schema": "auth"},
    )

    uuid: Mapped[str] = mapped_column(
        String(36),
        server_default=text("gen_random_uuid()"),
        primary_key=True,
    )
    client_id: Mapped[str | None] = mapped_column(Text)
    user_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_user.uuid", ondelete="CASCADE")
    )
    backend: Mapped[str | None] = mapped_column(Text)
    login: Mapped[str | None] = mapped_column(Text)
    user_agent: Mapped[str | None] = mapped_column(Text)
    remote_addr: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    mobile: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")

    @hybrid_property
    def tenant_uuid(self) -> str:
        return self.user.tenant_uuid

    @tenant_uuid.expression
    def tenant_uuid(cls):
        return (
            select(User.tenant_uuid)
            .where(User.uuid == cls.user_uuid)
            .label("tenant_uuid")
        )


class Session(Base):
    """Represents a user session."""

    __tablename__ = "auth_session"
    __table_args__ = (
        Index("auth_session__idx__tenant_uuid", "tenant_uuid"),
        {"schema": "auth"},
    )
    uuid: Mapped[str] = mapped_column(
        String(36),
        server_default=text("gen_random_uuid()"),
        primary_key=True,
    )
    tenant_uuid: Mapped[str] = mapped_column(
        String(38), ForeignKey("auth_tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    mobile: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    tokens: Mapped[list["Token"]] = relationship("Token", viewonly=True)


from accent_auth.users.models import (
    User,
)  # Import at the end to prevent circular import issues
