# Copyright 2023 Accent Communications

import marshmallow
from flask import request

from accent_auth import exceptions, http
from accent_auth.plugin_helpers.flask import extract_connection_params
from accent_auth.plugins.http.tenants.schemas import TenantFullSchema

from .schemas import UserRegisterPostSchema


class Register(http.ErrorCatchingResource):
    def __init__(self, email_service, tenant_service, user_service):
        self.email_service = email_service
        self.tenant_service = tenant_service
        self.user_service = user_service

    def post(self):
        try:
            args = UserRegisterPostSchema().load(request.get_json())
        except marshmallow.ValidationError as e:
            raise exceptions.UserParamException.from_errors(e.messages)

        tenant_body = TenantFullSchema().load({'name': args['username']})
        tenant = self.tenant_service.new(**tenant_body)
        result = self.user_service.new_user(
            enabled=True, tenant_uuid=tenant['uuid'], **args
        )

        try:
            address = args['email_address']
            for e in result['emails']:
                if e['address'] != address:
                    continue
                connection_params = extract_connection_params(request.headers)
                self.email_service.send_confirmation_email(
                    result['username'],
                    e['uuid'],
                    address,
                    connection_params,
                )
        except Exception:
            self.user_service.delete_user(tenant['uuid'], result['uuid'])
            raise

        return result, 200
