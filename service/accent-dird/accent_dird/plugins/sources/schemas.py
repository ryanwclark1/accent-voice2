# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import ListSchema as _ListSchema

from accent_dird.database.schemas import SourceSchema


class ListSchema(_ListSchema):
    searchable_columns = ['uuid', 'backend', 'name']
    sort_columns = ['name', 'backend']
    default_sort_column = 'name'

    recurse = fields.Boolean(missing=False)


source_list_schema = SourceSchema(many=True)
list_schema = ListSchema()
