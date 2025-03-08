# Copyright 2023 Accent Communications

from ...middleware import ResourceMiddleware
from .schema import ContextSchemaPUT


class ContextMiddleWare(ResourceMiddleware):
    def __init__(self, service):
        super().__init__(service, ContextSchemaPUT())

    def get(self, **criteria):
        model = self._service.get_by(**criteria)
        return self._schema.dump(model)

    def update(self, context_id, body, tenant_uuids):
        model = self._service.get(context_id, tenant_uuids=tenant_uuids)
        self.parse_and_update(model, body)
