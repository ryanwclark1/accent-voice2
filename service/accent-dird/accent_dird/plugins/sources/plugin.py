# Copyright 2023 Accent Communications

from accent_dird import BaseViewPlugin

from . import http


class SourcesViewPlugin(BaseViewPlugin):
    def load(self, dependencies):
        api = dependencies['api']
        source_service = dependencies['services']['source']

        api.add_resource(http.Sources, '/sources', resource_class_args=(source_service,))
