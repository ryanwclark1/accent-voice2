# Copyright 2023 Accent Communications

from marshmallow import fields, post_dump
from marshmallow.validate import Length, Regexp

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink, Nested

NAME_REGEX = r'^[-_.a-zA-Z0-9]+$'


class SkillSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    tenant_uuid = fields.String(dump_only=True)
    name = fields.String(validate=(Regexp(NAME_REGEX), Length(max=64)), required=True)
    description = fields.String(allow_none=True)
    links = ListLink(Link('skills'))

    agents = Nested(
        'SkillAgentsSchema', attribute='agent_queue_skills', many=True, dump_only=True
    )


class SkillAgentsSchema(BaseSchema):
    skill_weight = fields.Integer(attribute='weight')
    agent = Nested(
        'AgentSchema',
        only=['id', 'number', 'firstname', 'lastname', 'links'],
        dump_only=True,
    )

    @post_dump
    def merge_agent_queue_skills(self, data, **kwargs):
        agent = data.pop('agent', None)
        if not agent:
            return data

        data['id'] = agent.get('id', None)
        data['number'] = agent.get('number', None)
        data['firstname'] = agent.get('firstname', None)
        data['lastname'] = agent.get('lastname', None)
        data['links'] = agent.get('links', [])
        return data
