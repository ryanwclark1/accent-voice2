# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.client.plugin import ClientPlugin

from .http import Input, Lookup


class Plugin(ClientPlugin):
    vendor = 'polycom'
    import_name = __name__

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Input,
            self.input_url,
            endpoint='polycom_input',
            resource_class_kwargs=class_kwargs,
        )
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='polycom_lookup',
            resource_class_kwargs=class_kwargs,
        )
