# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['saml_config_service'],)

        api.add_resource(
            http.SAMLConfig,
            '/backends/saml',
            resource_class_args=args,
        )

        api.add_resource(
            http.SAMLMetadata,
            '/backends/saml/metadata',
            resource_class_args=args,
        )

        api.add_resource(
            http.SAMLAcsUrlTemplate,
            '/backends/saml/acs_url_template',
            resource_class_args=args,
        )
