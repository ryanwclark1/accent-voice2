# Copyright 2023 Accent Communications

from accent_deployd_client.command import DeploydCommand


class InstancesCommand(DeploydCommand):
    resource = 'instances'

    def __init__(self, client):
        super().__init__(client)

    def list(self, provider_uuid=None, **params):
        headers = self._get_headers(**params)
        if provider_uuid:
            url = self._provider_instances_all_url(provider_uuid)
        else:
            url = self._instances_all_url()

        response = self.session.get(url, headers=headers, params=params)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def _create_instance(self, url, instance_data, tenant_uuid):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        response = self.session.post(url, json=instance_data, headers=headers)
        if response.status_code != 201:
            self.raise_from_response(response)

        return response.json()

    def register(self, instance_data, tenant_uuid=None):
        url = self._instances_all_url()
        return self._create_instance(url, instance_data, tenant_uuid)

    def create(self, provider_uuid, instance_data, tenant_uuid=None):
        url = self._provider_instances_all_url(provider_uuid)
        return self._create_instance(url, instance_data, tenant_uuid)

    def get(self, instance_uuid, tenant_uuid=None):
        url = self._instances_one_url(instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = self.session.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def get_accent(self, instance_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._instances_accent_url(instance_uuid)

        response = self.session.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def update(self, instance_uuid, instance_data, tenant_uuid=None):
        url = self._instances_one_url(instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = self.session.put(url, json=instance_data, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def _delete_instance(self, url, tenant_uuid):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        response = self.session.delete(url, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    def unregister(self, instance_uuid, tenant_uuid=None):
        url = self._instances_one_url(instance_uuid)
        return self._delete_instance(url, tenant_uuid)

    def delete(self, provider_uuid, instance_uuid, tenant_uuid=None):
        url = self._provider_instances_one_url(
            instance_uuid,
            provider_uuid,
        )
        return self._delete_instance(url, tenant_uuid)

    def get_credential(self, instance_uuid, credential_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)
        response = self.session.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    def create_credential(self, instance_uuid, credential_data, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_all_url(instance_uuid)
        response = self.session.post(url, json=credential_data, headers=headers)
        if response.status_code != 201:
            self.raise_from_response(response)
        return response.json()

    def update_credential(
        self, instance_uuid, credential_uuid, credential_data, tenant_uuid=None
    ):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)
        response = self.session.put(url, json=credential_data, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()

    def delete_credential(self, instance_uuid, credential_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)
        response = self.session.delete(url, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    def _instances_all_url(self):
        return self.base_url

    def _instances_one_url(self, instance_uuid):
        return '{base_url}/{instance_uuid}'.format(
            base_url=self._instances_all_url(),
            instance_uuid=instance_uuid,
        )

    def _instances_accent_url(self, instance_uuid):
        return '{base_url}/accent'.format(
            base_url=self._instances_one_url(instance_uuid),
        )

    def _credentials_one_url(self, instance_uuid, credential_uuid):
        return '{base_url}/{instance_uuid}/credentials/{credential_uuid}'.format(
            base_url=self._instances_all_url(),
            instance_uuid=instance_uuid,
            credential_uuid=credential_uuid,
        )

    def _credentials_all_url(self, instance_uuid):
        return '{base_url}/{instance_uuid}/credentials'.format(
            base_url=self._instances_all_url(),
            instance_uuid=instance_uuid,
        )

    def _provider_instances_all_url(self, provider_uuid):
        return self._client.url('providers', provider_uuid, 'instances')

    def _provider_instances_one_url(self, instance_uuid, provider_uuid):
        return '{base_url}/{instance_uuid}'.format(
            base_url=self._provider_instances_all_url(provider_uuid),
            instance_uuid=instance_uuid,
        )
