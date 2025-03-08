# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length, NoneOf, Regexp

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink, Nested

from .storage import RESERVED_DIRECTORIES

ASTERISK_CATEGORY = 'system'
RESERVED_DIRECTORIES_ERROR = (
    "The following name are reserved for internal usage: {}".format(
        RESERVED_DIRECTORIES
    )
)
DIRECTORY_REGEX = r'^[a-zA-Z0-9]{1}[-_.a-zA-Z0-9]+$'


class SoundQueryParametersSchema(BaseSchema):
    format = fields.String()
    language = fields.String(validate=[Regexp(DIRECTORY_REGEX)])


class SoundFormatSchema(BaseSchema):
    format = fields.String()
    language = fields.String()
    tenant_uuid = fields.String()
    text = fields.String()
    path = fields.String()


class SoundFileSchema(BaseSchema):
    tenant_uuid = fields.String()
    name = fields.String()
    formats = Nested(SoundFormatSchema, many=True)


class SoundSchema(BaseSchema):
    tenant_uuid = fields.String()
    name = fields.String(
        validate=[
            Length(max=149, min=1),
            NoneOf([ASTERISK_CATEGORY]),
            NoneOf(RESERVED_DIRECTORIES, error=RESERVED_DIRECTORIES_ERROR),
            Regexp(DIRECTORY_REGEX),
        ],
        required=True,
    )
    files = Nested(SoundFileSchema, many=True, dump_only=True)

    links = ListLink(Link('sounds', field='name', target='category'))
