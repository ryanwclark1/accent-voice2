# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        api.add_resource(
            http.SAMLACS,
            '/saml/acs',
            resource_class_args=(dependencies['saml_service'],),
        )
        api.add_resource(
            http.SAMLSSO,
            '/saml/sso',
            resource_class_args=(dependencies['saml_service'],),
        )
        api.add_resource(
            http.SAMLLogout,
            '/saml/logout',
            resource_class_args=(
                dependencies['saml_service'],
                dependencies['token_service'],
            ),
        )
        api.add_resource(
            http.SAMLSLS,
            '/saml/sls',
            resource_class_args=(dependencies['saml_service'],),
        )
