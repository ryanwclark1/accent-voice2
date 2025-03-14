# Copyright 2023 Accent Communications

import marshmallow
from accent.auth_verifier import required_acl
from flask import request

from accent_auth import exceptions
from accent_auth.flask_helpers import Tenant
from accent_auth.http import AuthResource

from .schemas import ldap_config_edit_schema, ldap_config_schema


class LDAPConfig(AuthResource):
    def __init__(self, ldap_service):
        self._ldap_service = ldap_service

    @required_acl('auth.backends.ldap.read')
    def get(self):
        scoping_tenant = Tenant.autodetect()
        return ldap_config_schema.dump(self._ldap_service.get(scoping_tenant.uuid)), 200

    @required_acl('auth.backends.ldap.update')
    def put(self):
        scoping_tenant = Tenant.autodetect()
        try:
            body = ldap_config_edit_schema.load(request.get_json(force=True))
            body['tenant_uuid'] = scoping_tenant.uuid
            ldap_config = self._ldap_service.create_or_update(**body)
        except marshmallow.ValidationError as e:
            for field in e.messages:
                raise exceptions.InvalidInputException(field)
        return ldap_config_schema.dump(ldap_config), 200

    @required_acl('auth.backends.ldap.delete')
    def delete(self):
        scoping_tenant = Tenant.autodetect()
        self._ldap_service.delete(scoping_tenant.uuid)
        return '', 204
