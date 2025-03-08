# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import Schema


class Command(Schema):
    command = fields.String(required=True)


command_schema = Command()
