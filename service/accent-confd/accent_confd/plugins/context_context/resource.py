# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.helpers.exception import NotFoundError
from flask import request
from marshmallow import fields

from accent_confd.auth import required_acl
from accent_confd.helpers.mallow import BaseSchema, Nested
from accent_confd.helpers.restful import ConfdResource


class ContextSchemaIDLoad(BaseSchema):
    id = fields.Integer(required=True)


class ContextsSchema(BaseSchema):
    contexts = Nested(ContextSchemaIDLoad, many=True, required=True)


class ContextContextList(ConfdResource):
    schema = ContextsSchema

    def __init__(self, service, context_dao):
        super().__init__()
        self.service = service
        self.context_dao = context_dao

    @required_acl('confd.contexts.{context_id}.contexts.update')
    def put(self, context_id):
        context = self.context_dao.get(context_id)
        form = self.schema().load(request.get_json())
        try:
            contexts = [self.context_dao.get(c['id']) for c in form['contexts']]
        except NotFoundError as e:
            raise errors.param_not_found('contexts', 'Context', **e.metadata)

        self.service.associate_contexts(context, contexts)

        return '', 204
