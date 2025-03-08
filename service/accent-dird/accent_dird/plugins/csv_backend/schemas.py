# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow.validate import Length
from accent.mallow_helpers import ListSchema as _ListSchema

from accent_dird.schemas import BaseSourceSchema


class SourceSchema(BaseSourceSchema):
    unique_column = fields.String(
        validate=Length(min=1, max=128),
        allow_none=True,
        missing=None,
    )
    file = fields.String(validate=Length(min=1), required=True)
    separator = fields.String(validate=Length(min=1, max=1), missing=',')


class ListSchema(_ListSchema):
    searchable_columns = ['uuid', 'name', 'file']
    sort_columns = ['name', 'file']
    default_sort_column = 'name'

    recurse = fields.Boolean(missing=False)


source_list_schema = SourceSchema(many=True)
source_schema = SourceSchema()
list_schema = ListSchema()
