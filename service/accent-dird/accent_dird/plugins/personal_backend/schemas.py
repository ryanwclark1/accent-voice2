# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import ListSchema as _ListSchema

from accent_dird.schemas import BaseSourceSchema


class ListSchema(_ListSchema):
    searchable_columns = ['uuid', 'name']
    sort_columns = ['name']
    default_sort_column = 'name'

    recurse = fields.Boolean(missing=False)


source_list_schema = BaseSourceSchema(many=True)
source_schema = BaseSourceSchema()
list_schema = ListSchema()
