# Copyright 2023 Accent Communications

from .address import AddressDAO
from .domain import DomainDAO
from .email import EmailDAO
from .external_auth import ExternalAuthDAO
from .group import GroupDAO
from .ldap_config import LDAPConfigDAO
from .policy import PolicyDAO
from .refresh_token import RefreshTokenDAO
from .saml_config import SAMLConfigDAO
from .saml_pysaml2_cache import SAMLPysaml2CacheDAO
from .saml_session import SAMLSessionDAO
from .session import SessionDAO
from .tenant import TenantDAO
from .token import TokenDAO
from .user import UserDAO


class DAO:
    def __init__(
        self,
        address,
        domain,
        email,
        external_auth,
        group,
        ldap_config,
        policy,
        refresh_token,
        saml_config,
        saml_session,
        saml_pysaml2_cache,
        session,
        tenant,
        token,
        user,
    ):
        self.address = address
        self.domain = domain
        self.email = email
        self.external_auth = external_auth
        self.group = group
        self.ldap_config = ldap_config
        self.policy = policy
        self.refresh_token = refresh_token
        self.saml_config = saml_config
        self.saml_session = saml_session
        self.saml_pysaml2_cache = saml_pysaml2_cache
        self.session = session
        self.tenant = tenant
        self.token = token
        self.user = user

    @classmethod
    def from_defaults(cls):
        return cls(
            address=AddressDAO(),
            domain=DomainDAO(),
            email=EmailDAO(),
            external_auth=ExternalAuthDAO(),
            group=GroupDAO(),
            ldap_config=LDAPConfigDAO(),
            policy=PolicyDAO(),
            refresh_token=RefreshTokenDAO(),
            saml_config=SAMLConfigDAO(),
            saml_session=SAMLSessionDAO(),
            saml_pysaml2_cache=SAMLPysaml2CacheDAO(),
            session=SessionDAO(),
            tenant=TenantDAO(),
            token=TokenDAO(),
            user=UserDAO(),
        )
