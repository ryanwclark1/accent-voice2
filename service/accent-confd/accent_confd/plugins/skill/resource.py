# Copyright 2023 Accent Communications

from accent_dao.alchemy.queueskill import QueueSkill
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import SkillSchema


class SkillList(ListResource):
    model = QueueSkill
    schema = SkillSchema

    def build_headers(self, skill):
        return {'Location': url_for('skills', id=skill.id, _external=True)}

    @required_acl('confd.agents.skills.create')
    def post(self):
        return super().post()

    @required_acl('confd.agents.skills.read')
    def get(self):
        return super().get()


class SkillItem(ItemResource):
    schema = SkillSchema
    has_tenant_uuid = True

    @required_acl('confd.agents.skills.{id}.read')
    def get(self, id):
        return super().get(id)

    @required_acl('confd.agents.skills.{id}.update')
    def put(self, id):
        return super().put(id)

    @required_acl('confd.agents.skills.{id}.delete')
    def delete(self, id):
        return super().delete(id)
