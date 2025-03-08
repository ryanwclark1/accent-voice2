# Copyright 2023 Accent Communications


from accent.mallow_helpers import ListSchema as _ListSchema


class ListSchema(_ListSchema):
    searchable_columns = ['uuid', 'name', 'backend']
    sort_columns = ['name', 'backend']
    default_sort_column = 'name'
