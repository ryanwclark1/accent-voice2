# Copyright 2023 Accent Communications

from accent_dird import BaseViewPlugin

from . import http


class ProfilesViewPlugin(BaseViewPlugin):
    def load(self, dependencies):
        api = dependencies['api']
        profile_service = dependencies['services']['profile']

        api.add_resource(http.Profiles, '/profiles', resource_class_args=(profile_service,))

        api.add_resource(
            http.Profile,
            '/profiles/<profile_uuid>',
            resource_class_args=(profile_service,),
        )
