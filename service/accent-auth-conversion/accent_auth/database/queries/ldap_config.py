# Copyright 2023 Accent Communications

from sqlalchemy import exc

from ... import exceptions
from ..models import LDAPConfig
from .base import BaseDAO


class LDAPConfigDAO(BaseDAO):
    def get(self, tenant_uuid):
        ldap_config = (
            self.session.query(LDAPConfig)
            .filter(LDAPConfig.tenant_uuid == tenant_uuid)
            .first()
        )
        if ldap_config:
            return {
                'tenant_uuid': ldap_config.tenant_uuid,
                'host': ldap_config.host,
                'port': ldap_config.port,
                'protocol_version': ldap_config.protocol_version,
                'protocol_security': ldap_config.protocol_security,
                'bind_dn': ldap_config.bind_dn,
                'bind_password': ldap_config.bind_password,
                'user_base_dn': ldap_config.user_base_dn,
                'user_login_attribute': ldap_config.user_login_attribute,
                'user_email_attribute': ldap_config.user_email_attribute,
                'search_filters': ldap_config.search_filters,
            }
        raise exceptions.UnknownLDAPConfigException(tenant_uuid)

    def create(
        self,
        tenant_uuid,
        host,
        port,
        user_base_dn,
        user_login_attribute,
        user_email_attribute,
        protocol_version=3,
        protocol_security=None,
        bind_dn=None,
        bind_password=None,
        search_filters=None,
    ):
        ldap_config = LDAPConfig(
            tenant_uuid=tenant_uuid,
            host=host,
            port=port,
            user_base_dn=user_base_dn,
            user_login_attribute=user_login_attribute,
            user_email_attribute=user_email_attribute,
            protocol_version=protocol_version,
            protocol_security=protocol_security,
            bind_dn=bind_dn,
            bind_password=bind_password,
            search_filters=search_filters,
        )
        self.session.add(ldap_config)
        try:
            self.session.flush()
        except exc.IntegrityError as e:
            self.session.rollback()
            if e.orig.pgcode == self._UNIQUE_CONSTRAINT_CODE:
                raise exceptions.DuplicatedLDAPConfigException(tenant_uuid)
            raise
        return ldap_config.tenant_uuid

    def update(self, tenant_uuid, **kwargs):
        filter_ = LDAPConfig.tenant_uuid == str(tenant_uuid)
        ldap_config = self.get(tenant_uuid)
        ldap_config.update(kwargs)

        try:
            self.session.query(LDAPConfig).filter(filter_).update(ldap_config)
            self.session.flush()
        except exc.IntegrityError:
            self.session.rollback()
            raise

    def delete(self, tenant_uuid):
        filter_ = LDAPConfig.tenant_uuid == str(tenant_uuid)
        self.session.query(LDAPConfig).filter(filter_).delete(synchronize_session=False)
        self.session.flush()

    def exists(self, tenant_uuid):
        filter_ = LDAPConfig.tenant_uuid == str(tenant_uuid)
        return self.session.query(LDAPConfig).filter(filter_).count() > 0
