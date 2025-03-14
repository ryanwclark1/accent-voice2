# Copyright 2023 Accent Communications

from accent.tenant_flask_helpers import Tenant
from flask import request

from accent_calld.auth import get_token_user_uuid_from_request, required_acl
from accent_calld.http import AuthResource

from .schemas import (
    fax_creation_request_schema,
    fax_schema,
    user_fax_creation_request_schema,
)


class FaxesResource(AuthResource):
    def __init__(self, faxes_service):
        self._service = faxes_service

    @required_acl('calld.faxes.create')
    def post(self):
        tenant = Tenant.autodetect()
        fax_infos = fax_creation_request_schema.load(request.args)
        fax = self._service.send_fax(
            tenant.uuid, content=request.data, fax_infos=fax_infos
        )
        return fax_schema.dump(fax), 201


class UserFaxesResource(AuthResource):
    def __init__(self, faxes_service):
        self._service = faxes_service

    @required_acl('calld.users.me.faxes.create')
    def post(self):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        fax_infos = user_fax_creation_request_schema.load(request.args)
        fax = self._service.send_fax_from_user(
            tenant.uuid, user_uuid, content=request.data, fax_infos=fax_infos
        )
        return fax_schema.dump(fax), 201
