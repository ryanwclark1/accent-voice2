# Copyright 2023 Accent Communications

from accent.mallow import fields, validate
from accent.mallow_helpers import Schema


class AgentLoginSchema(Schema):
    extension = fields.String(required=True)
    context = fields.String(required=True)


class UserAgentLoginSchema(Schema):
    line_id = fields.Integer(required=True)


class PauseSchema(Schema):
    reason = fields.String(
        validate=validate.Length(min=1, max=80), missing=None, default=None
    )


class QueueSchema(Schema):
    queue_id = fields.Integer(required=True)


agent_login_schema = AgentLoginSchema()
pause_schema = PauseSchema()
queue_schema = QueueSchema()
user_agent_login_schema = UserAgentLoginSchema()
