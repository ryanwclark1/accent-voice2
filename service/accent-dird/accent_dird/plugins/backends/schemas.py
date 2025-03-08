# Copyright 2023 Accent Communications

from accent.mallow_helpers import ListSchema as _ListSchema


class ListSchema(_ListSchema):
    searchable_columns = ['name']
    sort_columns = ['name']
    default_sort_column = 'name'
