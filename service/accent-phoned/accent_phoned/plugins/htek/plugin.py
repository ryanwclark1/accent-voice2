# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.client.plugin import ClientPlugin

from .http import Lookup


class Plugin(ClientPlugin):
    vendor = 'htek'
    import_name = __name__

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='htek_lookup',
            resource_class_kwargs=class_kwargs,
        )
