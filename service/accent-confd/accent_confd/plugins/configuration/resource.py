# Copyright 2023 Accent Communications

from flask import request

from accent_confd.auth import required_acl, required_master_tenant
from accent_confd.helpers.mallow import BaseSchema, StrictBoolean
from accent_confd.helpers.restful import ConfdResource


class LiveReloadSchema(BaseSchema):
    enabled = StrictBoolean(required=True)


class LiveReloadResource(ConfdResource):
    schema = LiveReloadSchema

    def __init__(self, service):
        super().__init__()
        self.service = service

    @required_master_tenant()
    @required_acl('confd.configuration.live_reload.read')
    def get(self):
        model = self.service.get()
        return self.schema().dump(model)

    @required_master_tenant()
    @required_acl('confd.configuration.live_reload.update')
    def put(self):
        form = self.schema().load(request.get_json())
        self.service.edit(form)
        return '', 204
