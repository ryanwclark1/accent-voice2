# accent_auth/db/__init__.py

from .base import Base
from .engine import AsyncSessionLocal, async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

# Import all DAO classes
from accent_auth.auth.service import TokenDAO, RefreshTokenDAO, SessionDAO

from accent_auth.users.service import (
    UserDAO,
    EmailDAO,
    UserExternalAuthDAO,
    UserGroupDAO,
    UserPolicyDAO,
)

from accent_auth.tenants.service import (
    TenantDAO,
    DomainDAO,
    AddressDAO,
    GroupDAO,
    PolicyDAO,
    GroupPolicyDAO,
    ExternalAuthTypeDAO,
    ExternalAuthConfigDAO,
    LDAPConfigDAO,
    SAMLConfigDAO,
    SAMLSessionDAO,
    SAMLPysaml2CacheDAO,
    PolicyAccessDAO,
)


class DAO:
    """
    Aggregates all Data Access Objects (DAOs) for convenient access.
    """

    def __init__(
        self,
        token: TokenDAO,
        refresh_token: RefreshTokenDAO,
        session: SessionDAO,
        user: UserDAO,
        email: EmailDAO,
        external_auth: UserExternalAuthDAO,
        user_group: UserGroupDAO,
        user_policy: UserPolicyDAO,
        tenant: TenantDAO,
        domain: DomainDAO,
        address: AddressDAO,
        group: GroupDAO,
        policy: PolicyDAO,
        group_policy: GroupPolicyDAO,
        external_auth_type: ExternalAuthTypeDAO,
        external_auth_config: ExternalAuthConfigDAO,
        ldap_config: LDAPConfigDAO,
        saml_config: SAMLConfigDAO,
        saml_session: SAMLSessionDAO,
        saml_pysaml2_cache: SAMLPysaml2CacheDAO,
        policy_access: PolicyAccessDAO,
    ):
        self.token = token
        self.refresh_token = refresh_token
        self.session = session
        self.user = user
        self.email = email
        self.external_auth = external_auth
        self.group = group
        self.user_group = user_group
        self.user_policy = user_policy
        self.tenant = tenant
        self.domain = domain
        self.address = address
        self.policy = policy
        self.group_policy = group_policy
        self.external_auth_type = external_auth_type
        self.external_auth_config = external_auth_config
        self.ldap_config = ldap_config
        self.saml_config = saml_config
        self.saml_session = saml_session
        self.saml_pysaml2_cache = saml_pysaml2_cache
        self.policy_access = policy_access

    @classmethod
    def from_defaults(cls) -> "DAO":
        """Creates a DAO instance with default DAO implementations."""
        return cls(
            token=TokenDAO(),
            refresh_token=RefreshTokenDAO(),
            session=SessionDAO(),
            user=UserDAO(),
            email=EmailDAO(),
            external_auth=UserExternalAuthDAO(),
            user_group=UserGroupDAO(),
            user_policy=UserPolicyDAO(),
            tenant=TenantDAO(),
            domain=DomainDAO(),
            address=AddressDAO(),
            group=GroupDAO(),
            policy=PolicyDAO(),
            group_policy=GroupPolicyDAO(),
            external_auth_type=ExternalAuthTypeDAO(),
            external_auth_config=ExternalAuthConfigDAO(),
            ldap_config=LDAPConfigDAO(),
            saml_config=SAMLConfigDAO(),
            saml_session=SAMLSessionDAO(),
            saml_pysaml2_cache=SAMLPysaml2CacheDAO(),
            policy_access=PolicyAccessDAO(),
        )

    async def get_db_session(self) -> AsyncSession:  # Added method
        """
        Returns: An instance of AsyncSession
        """
        return AsyncSessionLocal()

    async def find_top_tenant(self, session: AsyncSession):
        """Finds the top-level tenant."""
        result = await session.execute(
            select(self.tenant.model).where(
                self.tenant.model.uuid == self.tenant.model.parent_uuid
            )
        )
        return result.scalar_one()

    async def list_visible_tenants(self, top_tenant_uuid: str, session: AsyncSession):
        """Lists all visible tenants for service discovery"""
        query = await self.tenant._tenant_tree_query(top_tenant_uuid)
        result = await session.execute(query)  # Execute the query with the session
        return result.scalars().all()

    async def count(self, session: AsyncSession, **kwargs) -> int:
        """Return total count of rows in the model's table."""
        query = select(func.count(self.model.id))  # Use self.model.id

        if kwargs:
            query = query.filter_by(**kwargs)
        result = await session.execute(query)  # Execute the query
        return result.scalar_one()  # Use first() to get a single row
