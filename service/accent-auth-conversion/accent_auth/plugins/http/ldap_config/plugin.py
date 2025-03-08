# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['ldap_service'],)

        api.add_resource(
            http.LDAPConfig,
            '/backends/ldap',
            resource_class_args=args,
        )
