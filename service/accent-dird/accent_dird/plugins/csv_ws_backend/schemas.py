# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow.validate import Length, Range
from accent.mallow_helpers import ListSchema as _ListSchema

from accent_dird.schemas import BaseSourceSchema, VerifyCertificateField


class SourceSchema(BaseSourceSchema):
    lookup_url = fields.URL(required=True)
    list_url = fields.URL(allow_none=True, missing=None)
    verify_certificate = VerifyCertificateField(missing=True)
    delimiter = fields.String(validate=Length(min=1, max=1), missing=',')
    timeout = fields.Float(validate=Range(min=0), missing=10.0)
    unique_column = fields.String(validate=Length(min=1, max=128), allow_none=True, missing=None)


class ListSchema(_ListSchema):
    searchable_columns = ['uuid', 'name', 'lookup_url', 'list_url']
    sort_columns = ['name', 'lookup_url', 'list_url']
    default_sort_column = 'name'

    recurse = fields.Boolean(missing=False)


source_list_schema = SourceSchema(many=True)
source_schema = SourceSchema()
list_schema = ListSchema()
