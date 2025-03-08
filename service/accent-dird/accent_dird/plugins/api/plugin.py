# Copyright 2023 Accent Communications

from accent_dird import BaseViewPlugin

from . import http


class ApiViewPlugin(BaseViewPlugin):
    def load(self, dependencies):
        api = dependencies['api']
        api.add_resource(http.ApiResource, '/api/api.yml')
