# Copyright 2023 Accent Communications

from marshmallow import fields, post_dump
from marshmallow.validate import Length, Predicate

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink, Nested


class PagingSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    tenant_uuid = fields.String(dump_only=True)
    number = fields.String(
        validate=(Length(max=32), Predicate('isdigit')), required=True
    )
    name = fields.String(validate=Length(max=128), allow_none=True)
    announce_caller = fields.Boolean()
    announce_sound = fields.String(validate=Length(max=64), allow_none=True)
    caller_notification = fields.Boolean()
    duplex = fields.Boolean(attribute='duplex_bool')
    ignore_forward = fields.Boolean()
    record = fields.Boolean(attribute='record_bool')
    enabled = fields.Boolean()
    links = ListLink(Link('pagings'))

    users_caller = Nested(
        'UserSchema',
        only=['uuid', 'firstname', 'lastname', 'links'],
        many=True,
        dump_only=True,
    )
    users_member = Nested(
        'UserSchema',
        only=['uuid', 'firstname', 'lastname', 'links'],
        many=True,
        dump_only=True,
    )

    @post_dump
    def wrap_users(self, data, **kwargs):
        users_member = data.pop('users_member', [])
        users_caller = data.pop('users_caller', [])

        if not self.only or 'members' in self.only:
            data['members'] = {'users': users_member}
        if not self.only or 'callers' in self.only:
            data['callers'] = {'users': users_caller}

        return data
