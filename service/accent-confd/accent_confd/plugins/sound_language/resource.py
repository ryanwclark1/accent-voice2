# Copyright 2023 Accent Communications

from marshmallow import fields

from accent_confd.auth import required_acl
from accent_confd.helpers.mallow import BaseSchema
from accent_confd.helpers.restful import ListResource


class SoundLanguageSchema(BaseSchema):
    tag = fields.String(dump_only=True)


class SoundLanguageList(ListResource):
    schema = SoundLanguageSchema

    @required_acl('confd.sounds.languages.get')
    def get(self):
        return super().get()

    def post(self, id):
        return '', 405
