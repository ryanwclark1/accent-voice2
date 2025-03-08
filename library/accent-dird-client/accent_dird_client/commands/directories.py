# Copyright 2023 Accent Communications

import logging

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand

logger = logging.getLogger(__name__)


class DirectoriesCommand(DirdRESTCommand):
    resource = 'directories'

    def lookup(self, profile, token=None, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/lookup/{profile}'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def lookup_user(self, profile, user_uuid, token=None, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/lookup/{profile}/{user_uuid}'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def reverse(self, profile, user_uuid=None, token=None, tenant_uuid=None, **kwargs):
        if not user_uuid and 'accent_user_uuid' in kwargs:
            logger.warning(
                'The "accent_user_uuid" argument has been renamed to "user_uuid"'
            )
            user_uuid = kwargs.pop('accent_user_uuid')

        url = f'{self.base_url}/reverse/{profile}/{user_uuid}'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def headers(self, profile, token=None, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/lookup/{profile}/headers'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def favorites(self, profile, token=None, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/favorites/{profile}'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def new_favorite(self, directory, contact, token=None, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/favorites/{directory}/{contact}'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.put(url, params=kwargs, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def remove_favorite(
        self, directory, contact, token=None, tenant_uuid=None, **kwargs
    ):
        url = f'{self.base_url}/favorites/{directory}/{contact}'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.delete(url, params=kwargs, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def personal(self, profile, token=None, tenant_uuid=None, **kwargs):
        url = f'{self.base_url}/personal/{profile}'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_sources(self, profile, token=None, tenant_uuid=None, **list_params):
        url = f'{self.base_url}/{profile}/sources'
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=list_params, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
