# Copyright 2023 Accent Communications

from marshmallow import fields, post_load, pre_dump
from marshmallow.validate import Length

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink, Nested


class SkillRuleSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    tenant_uuid = fields.String(dump_only=True)
    name = fields.String(validate=(Length(max=64)), required=True)
    rules = Nested('SkillRuleRuleSchema', many=True, allow_none=True)
    links = ListLink(Link('skillrules'))


class SkillRuleRuleSchema(BaseSchema):
    definition = fields.String(required=True)

    @post_load
    def remove_envelope(self, data, **kwargs):
        return data['definition']

    @pre_dump
    def add_envelope(self, data, **kwargs):
        return {'definition': data}
