# Copyright 2023 Accent Communications

from flask import request
from marshmallow import fields, validates_schema
from marshmallow.exceptions import ValidationError

from accent_confd.auth import required_acl
from accent_confd.helpers.mallow import BaseSchema, Nested
from accent_confd.helpers.restful import ConfdResource


class GroupSchemaIDUUIDLoad(BaseSchema):
    id = fields.Integer()
    uuid = fields.UUID()

    @validates_schema
    def _validate_at_least_one_identifier(self, data, **kwargs):
        _id = data.get('id')
        uuid = data.get('uuid')

        provided_identifiers = [identifier for identifier in [_id, uuid] if identifier]
        if len(provided_identifiers) == 0:
            raise ValidationError('One identifier(id or uuid) must be provided')


class GroupsIDUUIDSchema(BaseSchema):
    groups = Nested(
        GroupSchemaIDUUIDLoad, many=True, required=True, partial=['id', 'uuid']
    )


class UserGroupItem(ConfdResource):
    schema = GroupsIDUUIDSchema

    def __init__(self, service, middleware):
        super().__init__()
        self.service = service
        self._middleware = middleware

    @required_acl('confd.users.{user_id}.groups.update')
    def put(self, user_id):
        self._middleware.associate_all_groups(request.get_json(), user_id)
        return '', 204
