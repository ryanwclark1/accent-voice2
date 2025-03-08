# Copyright 2023 Accent Communications

from marshmallow import fields

from accent_confd.auth import required_acl
from accent_confd.helpers.mallow import BaseSchema
from accent_confd.helpers.restful import ConfdResource


class InfoSchema(BaseSchema):
    uuid = fields.UUID()
    accent_version = fields.String()


class Info(ConfdResource):
    schema = InfoSchema

    def __init__(self, service):
        super().__init__()
        self.service = service

    @required_acl('confd.infos.read')
    def get(self):
        info = self.service.get()
        return self.schema().dump(info)
