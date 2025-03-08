# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow.validate import Length
from accent.mallow_helpers import ListSchema as _ListSchema

from accent_dird.schemas import BaseAuthConfigSchema, BaseSourceSchema


class SourceSchema(BaseSourceSchema):
    auth = fields.Nested(
        BaseAuthConfigSchema,
        missing=lambda: BaseAuthConfigSchema().load({}),
    )
    endpoint = fields.String(
        missing='https://graph.microsoft.com/v1.0/me/contacts',
        validate=Length(min=1, max=255),
    )


class ListSchema(_ListSchema):
    searchable_columns = ['uuid', 'name']
    sort_columns = ['name']
    default_sort_column = 'name'

    recurse = fields.Boolean(missing=False)


class ContactListSchema(_ListSchema):
    searchable_columns = ['displayName', 'givenName', 'surname']
    sort_columns = ['displayName', 'givenName', 'surname']
    default_sort_column = 'displayName'


source_schema = SourceSchema()
source_list_schema = SourceSchema(many=True)
list_schema = ListSchema()
contact_list_schema = ContactListSchema()
