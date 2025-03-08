# Copyright 2023 Accent Communications

from .helpers.base_command import DirdRESTCommand


class PhonebookCommand(DirdRESTCommand):
    resource = 'phonebooks'

    def create(self, token=None, phonebook_body=None, tenant_uuid=None, **kwargs):
        url = self._phonebook_all_url()
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.post(url, json=phonebook_body, params=kwargs, headers=headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def create_contact(
        self,
        token=None,
        phonebook_uuid=None,
        contact_body=None,
        tenant_uuid=None,
        **kwargs,
    ):
        url = self._contact_all_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.post(url, json=contact_body, params=kwargs, headers=headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def list(self, token=None, tenant_uuid=None, **kwargs):
        url = self._phonebook_all_url()
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_contacts(
        self, token=None, phonebook_uuid=None, tenant_uuid=None, **kwargs
    ):
        url = self._contact_all_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def delete(self, token=None, phonebook_uuid=None, tenant_uuid=None, **kwargs):
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.delete(url, params=kwargs, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(
        self,
        token=None,
        phonebook_uuid=None,
        phonebook_body=None,
        tenant_uuid=None,
        **kwargs,
    ):
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.put(url, json=phonebook_body, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, token=None, phonebook_uuid=None, tenant_uuid=None, **kwargs):
        url = self._phonebook_one_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_contact(
        self,
        token=None,
        phonebook_uuid=None,
        contact_uuid=None,
        tenant_uuid=None,
        **kwargs,
    ):
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.get(url, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def edit_contact(
        self,
        token=None,
        phonebook_uuid=None,
        contact_uuid=None,
        contact_body=None,
        tenant_uuid=None,
        **kwargs,
    ):
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.put(url, json=contact_body, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def delete_contact(
        self,
        token=None,
        phonebook_uuid=None,
        contact_uuid=None,
        tenant_uuid=None,
        **kwargs,
    ):
        url = self._contact_one_url(phonebook_uuid, contact_uuid)
        headers = self.build_headers(tenant_uuid, token)
        r = self.session.delete(url, params=kwargs, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def import_csv(
        self,
        phonebook_uuid=None,
        csv_text=None,
        encoding=None,
        token=None,
        tenant_uuid=None,
        **kwargs,
    ):
        url = self._contact_import_url(phonebook_uuid)
        headers = self.build_headers(tenant_uuid, token)
        content_type = f'text/csv; charset={encoding}' if encoding else 'text/csv'
        headers['Content-Type'] = content_type
        r = self.session.post(url, data=csv_text, params=kwargs, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def _contact_all_url(self, phonebook_uuid):
        return f'{self._phonebook_one_url(phonebook_uuid)}/contacts'

    def _contact_one_url(self, phonebook_uuid, contact_uuid):
        return f'{self._contact_all_url(phonebook_uuid)}/{contact_uuid}'

    def _contact_import_url(self, phonebook_uuid):
        return f'{self._contact_all_url(phonebook_uuid)}/import'

    def _phonebook_all_url(self):
        return f'{self.base_url}'

    def _phonebook_one_url(self, phonebook_uuid):
        return f'{self._phonebook_all_url()}/{phonebook_uuid}'
