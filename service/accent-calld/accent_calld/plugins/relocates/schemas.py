# Copyright 2023 Accent Communications

from marshmallow import EXCLUDE, Schema, ValidationError, fields
from marshmallow.validate import Length, OneOf, Range

VALID_COMPLETIONS = [
    'answer',
    'api',
]


class LineLocationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    line_id = fields.Integer(validate=Range(min=1), required=True)
    contact = fields.String()


class LocationField(fields.Field):
    class Meta:
        unknown = EXCLUDE

    locations = {
        'line': fields.Nested(LineLocationSchema),
        'mobile': None,
    }

    def _deserialize(self, value, attr, data, **kwargs):
        destination = data.get('destination')
        try:
            concrete_location = self.locations.get(destination)
        except TypeError:
            raise ValidationError(
                {
                    'message': 'Invalid destination',
                    'constraint_id': 'destination-type',
                    'constraint': {
                        'type': 'string',
                    },
                }
            )

        if not concrete_location:
            return {}
        return concrete_location._deserialize(value, attr, data)


class UserRelocateRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    initiator_call = fields.Str(validate=Length(min=1), required=True)
    destination = fields.Str(validate=OneOf(LocationField.locations))
    location = LocationField(missing=dict)
    completions = fields.List(
        fields.Str(validate=OneOf(VALID_COMPLETIONS)), missing=['answer']
    )
    timeout = fields.Integer(validate=Range(min=1), missing=30)
    auto_answer = fields.Boolean(missing=False)


user_relocate_request_schema = UserRelocateRequestSchema()


class RelocateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    uuid = fields.Str(validate=Length(equal=36), required=True)
    relocated_call = fields.Str(
        validate=Length(min=1), required=True, attribute='relocated_channel'
    )
    initiator_call = fields.Str(
        validate=Length(min=1), required=True, attribute='initiator_channel'
    )
    recipient_call = fields.Str(
        validate=Length(min=1), required=True, attribute='recipient_channel'
    )
    completions = fields.List(
        fields.Str(validate=OneOf(VALID_COMPLETIONS)), missing=['answer']
    )
    initiator = fields.Str(validate=Length(equal=36), required=True)
    timeout = fields.Integer(validate=Range(min=1), missing=30)
    auto_answer = fields.Boolean(missing=False)


relocate_schema = RelocateSchema()
