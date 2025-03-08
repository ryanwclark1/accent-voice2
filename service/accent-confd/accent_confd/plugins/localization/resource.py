# Copyright 2023 Accent Communications

from accent.tenant_flask_helpers import Tenant
from flask import request

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource, build_tenant

from .schema import LocalizationSchema


class LocalizationResource(ConfdResource):
    schema = LocalizationSchema

    def __init__(self, service):
        self.service = service

    @required_acl('confd.localization.read')
    def get(self):
        tenant = Tenant.autodetect()
        model = self.service.get(tenant.uuid)
        return self.schema().dump(model)

    @required_acl('confd.localization.update')
    def put(self):
        tenant_uuid = build_tenant()
        model = self.service.get(tenant_uuid)
        self._parse_and_update(model)
        return '', 204

    def _parse_and_update(self, model, **kwargs):
        form = self.schema().load(request.get_json(), partial=True)
        for name, value in form.items():
            setattr(model, name, value)
        self.service.edit(model, **kwargs)
