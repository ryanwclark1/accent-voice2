# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import ListSchema as _ListSchema

from accent_dird.database.schemas import DisplaySchema


class ListSchema(_ListSchema):
    searchable_columns = ['uuid', 'name']
    sort_columns = ['name']
    default_sort_column = 'name'

    recurse = fields.Boolean(missing=False)


display_list_schema = DisplaySchema(many=True)
display_schema = DisplaySchema()
list_schema = ListSchema()
