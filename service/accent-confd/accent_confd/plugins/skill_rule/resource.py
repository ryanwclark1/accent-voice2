# Copyright 2023 Accent Communications

from accent_dao.alchemy.queueskillrule import QueueSkillRule
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import SkillRuleSchema


class SkillRuleList(ListResource):
    model = QueueSkillRule
    schema = SkillRuleSchema

    def build_headers(self, skill_rule):
        return {'Location': url_for('skillrules', id=skill_rule.id, _external=True)}

    @required_acl('confd.queues.skillrules.create')
    def post(self):
        return super().post()

    @required_acl('confd.queues.skillrules.read')
    def get(self):
        return super().get()


class SkillRuleItem(ItemResource):
    schema = SkillRuleSchema
    has_tenant_uuid = True

    @required_acl('confd.queues.skillrules.{id}.read')
    def get(self, id):
        return super().get(id)

    @required_acl('confd.queues.skillrules.{id}.update')
    def put(self, id):
        return super().put(id)

    @required_acl('confd.queues.skillrules.{id}.delete')
    def delete(self, id):
        return super().delete(id)
