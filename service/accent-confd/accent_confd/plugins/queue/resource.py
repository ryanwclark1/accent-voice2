# Copyright 2023 Accent Communications

from accent_dao.alchemy.queuefeatures import QueueFeatures as Queue
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import QueueSchema, QueueSchemaPUT


class QueueList(ListResource):
    model = Queue
    schema = QueueSchema

    def build_headers(self, queue):
        return {'Location': url_for('queues', id=queue.id, _external=True)}

    @required_acl('confd.queues.create')
    def post(self):
        return super().post()

    @required_acl('confd.queues.read')
    def get(self):
        return super().get()


class QueueItem(ItemResource):
    schema = QueueSchemaPUT
    has_tenant_uuid = True

    @required_acl('confd.queues.{id}.read')
    def get(self, id):
        return super().get(id)

    @required_acl('confd.queues.{id}.update')
    def put(self, id):
        return super().put(id)

    @required_acl('confd.queues.{id}.delete')
    def delete(self, id):
        return super().delete(id)
