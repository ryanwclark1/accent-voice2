# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length, OneOf, Predicate

from accent_confd.helpers.mallow import BaseSchema
from accent_confd.helpers.restful import ListSchema as BaseListSchema


class ListSchema(BaseListSchema):
    availability = fields.String(
        missing='available', validate=OneOf(['available', 'all'])
    )


class ContextRangeSchema(BaseSchema):
    start = fields.String(
        validate=(Predicate('isdigit'), Length(max=16)), required=True
    )
    end = fields.String(validate=(Predicate('isdigit'), Length(max=16)))
