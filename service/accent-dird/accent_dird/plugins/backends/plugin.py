# Copyright 2023 Accent Communications

from accent_dird import BaseViewPlugin

from . import http, service


class BackendsViewPlugin(BaseViewPlugin):
    def load(self, dependencies):
        api = dependencies['api']
        backend_service = service.BackendService(dependencies['config'])

        api.add_resource(http.Backends, '/backends', resource_class_args=(backend_service,))
