# Copyright 2023 Accent Communications

from accent.mallow_helpers import Schema, fields


class EndpointBaseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    type = fields.String()
    technology = fields.String(default='unknown')
    registered = fields.Boolean(default=None)
    current_call_count = fields.Integer(default=None)


class LineEndpointSchema(EndpointBaseSchema):
    pass


class TrunkEndpointSchema(EndpointBaseSchema):
    pass


trunk_endpoint_schema = TrunkEndpointSchema()
line_endpoint_schema = LineEndpointSchema()
