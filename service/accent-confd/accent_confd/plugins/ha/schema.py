# Copyright 2023 Accent Communications

from accent.mallow import fields
from marshmallow import validates_schema
from marshmallow.exceptions import ValidationError
from marshmallow.validate import OneOf

from accent_confd.helpers.mallow import BaseSchema


class HASchema(BaseSchema):
    node_type = fields.String(
        validate=OneOf(['disabled', 'master', 'slave']), required=True
    )
    remote_address = fields.IP()

    @validates_schema
    def check_remote_if_enabled(self, data, **kwargs):
        if 'node_type' not in data:
            return
        if data['node_type'] == 'disabled':
            return

        if not data.get('remote_address'):
            raise ValidationError('remote_address cannot be empty')
