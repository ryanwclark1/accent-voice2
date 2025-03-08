# Copyright 2023 Accent Communications

from accent_deployd_client.command import DeploydCommand


class PlatformsSubcommand(DeploydCommand):
    resource = 'platforms'

    def __init__(self, client, base_url):
        super().__init__(client)
        self.base_url = base_url

    def list(self):
        headers = self._get_headers()
        url = self._providers_platforms_url()
        response = self.session.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def _providers_platforms_url(self):
        return '{base_url}/platforms'.format(
            base_url=self.base_url,
        )


class ProvidersCommand(DeploydCommand):
    resource = 'providers'

    def __init__(self, client):
        super().__init__(client)
        self.platforms = PlatformsSubcommand(
            client,
            self.base_url,
        )

    def list(self, **params):
        url = self._providers_all_url()
        headers = self._get_headers(**params)

        response = self.session.get(url, headers=headers, params=params)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def create(self, provider_data, tenant_uuid=None):
        url = self._providers_all_url()
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = self.session.post(url, json=provider_data, headers=headers)
        if response.status_code != 201:
            self.raise_from_response(response)

        return response.json()

    def get(self, provider_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._providers_one_url(provider_uuid)

        response = self.session.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def update(self, provider_uuid, provider_data, tenant_uuid=None):
        url = self._providers_one_url(provider_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = self.session.put(url, json=provider_data, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def delete(self, provider_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._providers_one_url(provider_uuid)

        response = self.session.delete(url, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    def list_images(self, provider_uuid, **params):
        return self._providers_resources('images', provider_uuid, **params)

    def list_locations(self, provider_uuid, **params):
        return self._providers_resources('locations', provider_uuid, **params)

    def list_key_pairs(self, provider_uuid, **params):
        return self._providers_resources('keypairs', provider_uuid, **params)

    def list_networks(self, provider_uuid, **params):
        return self._providers_resources('networks', provider_uuid, **params)

    def list_sizes(self, provider_uuid, **params):
        return self._providers_resources('sizes', provider_uuid, **params)

    def list_subnets(self, provider_uuid, **params):
        return self._providers_resources('subnets', provider_uuid, **params)

    def list_regions(self, provider_uuid, **params):
        return self._providers_resources('regions', provider_uuid, **params)

    def _providers_all_url(self):
        return self.base_url

    def _providers_one_url(self, provider_uuid):
        return '{base_url}/{provider_uuid}'.format(
            base_url=self._providers_all_url(),
            provider_uuid=provider_uuid,
        )

    def _providers_resources(self, endpoint, provider_uuid, tenant_uuid=None, **params):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = '{base_url}/{endpoint}'.format(
            base_url=self._providers_one_url(provider_uuid), endpoint=endpoint
        )

        response = self.session.get(url, headers=headers, params=params)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()