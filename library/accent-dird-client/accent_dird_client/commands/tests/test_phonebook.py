# Copyright 2023 Accent Communications

from unittest.mock import sentinel as s
from uuid import uuid4

from hamcrest import assert_that, equal_to, none
from accent_lib_rest_client.tests.command import RESTCommandTestCase

from ..phonebook import PhonebookCommand


class TestPhonebookContact(RESTCommandTestCase):
    Command = PhonebookCommand
    command: PhonebookCommand

    def setUp(self):
        super().setUp()
        self.tenant = str(uuid4())
        self.phonebook_uuid = str(uuid4())

    def test_create(self):
        self.session.post.return_value = self.new_response(
            201, json={'return': 'value'}
        )
        contact_body = {'firstname': 'Foo', 'lastname': 'Bar'}

        result = self.command.create_contact(
            phonebook_uuid=self.phonebook_uuid,
            token=s.token,
            contact_body=contact_body,
            tenant_uuid=self.tenant,
        )

        url = f'{self.base_url}/{self.phonebook_uuid}/contacts'
        self.session.post.assert_called_once_with(
            url,
            json=contact_body,
            params={},
            headers={
                'Accept': 'application/json',
                'X-Auth-Token': s.token,
                'Accent-Tenant': self.tenant,
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_create_when_not_201(self):
        self.session.post.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.create,
            phonebook_body={},
            tenant_uuid=self.tenant,
            token=s.token,
        )

    def test_list(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.list_contacts(
            tenant_uuid=self.tenant, token=s.token, phonebook_uuid=self.phonebook_uuid
        )

        url = f'{self.base_url}/{self.phonebook_uuid}/contacts'
        self.session.get.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Accent-Tenant': self.tenant,
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_list_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.list_contacts,
            token=s.token,
            tenant_uuid=self.tenant,
            phonebook_uuid=self.phonebook_uuid,
        )

    def test_get(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.get_contact(
            token=s.token,
            tenant_uuid=self.tenant,
            phonebook_uuid=self.phonebook_uuid,
            contact_uuid=s.contact_uuid,
        )

        url = f'{self.base_url}/' f'{self.phonebook_uuid}/contacts/{s.contact_uuid}'
        self.session.get.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Accent-Tenant': self.tenant,
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_get_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.get_contact,
            token=s.token,
            tenant_uuid=self.tenant,
            phonebook_uuid=self.phonebook_uuid,
            contact_uuid=s.contact_uuid,
        )

    def test_edit(self):
        self.session.put.return_value = self.new_response(200, json={'return': 'value'})
        body = {'firstname': 'test'}

        result = self.command.edit_contact(
            tenant_uuid=self.tenant,
            phonebook_uuid=self.phonebook_uuid,
            contact_uuid=s.contact_uuid,
            contact_body=body,
            token=s.token,
        )

        url = f'{self.base_url}/' f'{self.phonebook_uuid}/contacts/{s.contact_uuid}'

        self.session.put.assert_called_once_with(
            url,
            json=body,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Accent-Tenant': self.tenant,
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_edit_when_not_200(self):
        self.session.put.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.edit_contact)

    def test_delete(self):
        self.session.delete.return_value = self.new_response(204)

        result = self.command.delete_contact(
            tenant_uuid=self.tenant,
            phonebook_uuid=self.phonebook_uuid,
            contact_uuid=s.contact_uuid,
            token=s.token,
        )

        url = f'{self.base_url}/' f'{self.phonebook_uuid}/contacts/{s.contact_uuid}'
        self.session.delete.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Accent-Tenant': self.tenant,
            },
        )
        assert_that(result, none())

    def test_delete_when_not_204(self):
        self.session.delete.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.delete,
            token=s.token,
            tenant_uuid=s.tenant,
            phonebook_uuid=s.phonebook_uuid,
        )


class TestPhonebook(RESTCommandTestCase):
    Command = PhonebookCommand

    def test_create(self):
        self.session.post.return_value = self.new_response(
            201, json={'return': 'value'}
        )
        phonebook_body = {'name': 'main', 'description': 'The main phonebook'}
        tenant = 'mytenant'

        result = self.command.create(
            tenant_uuid=tenant, token=s.token, phonebook_body=phonebook_body
        )

        url = f'{self.base_url}'
        self.session.post.assert_called_once_with(
            url,
            json=phonebook_body,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Accent-Tenant': tenant,
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_create_when_not_201(self):
        self.session.post.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.create,
            phonebook_body={'name': 'main'},
            tenant_uuid='thetenant',
            token=s.token,
        )

    def test_list_phonebook(self):
        tenant = 'mytenant'
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.list(tenant_uuid=tenant, token=s.token)

        url = f'{self.base_url}'
        self._assert_get(url=url, token=s.token, tenant=tenant)
        assert_that(result, equal_to({'return': 'value'}))

    def test_list_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.list, s.token, 'mytenant')

    def test_get(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        tenant, phonebook_uuid = 'atenant', 42

        result = self.command.get(
            token=s.token, tenant_uuid=tenant, phonebook_uuid=phonebook_uuid
        )

        url = f'{self.base_url}/{phonebook_uuid}'
        self._assert_get(url, s.token, tenant)
        assert_that(result, equal_to({'return': 'value'}))

    def test_get_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.get,
            token=s.token,
            tenant_uuid='mytenant',
            phonebook_uuid=42,
        )

    def test_edit(self):
        self.session.put.return_value = self.new_response(200, json={'return': 'value'})
        tenant = 'thetenant'
        phonebook_uuid = 'my_contact_id'
        body = {'name': 'test'}

        result = self.command.edit(
            tenant_uuid=tenant,
            phonebook_uuid=phonebook_uuid,
            phonebook_body=body,
            token=s.token,
        )

        url = f'{self.base_url}/{phonebook_uuid}'
        self.session.put.assert_called_once_with(
            url,
            json=body,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Accent-Tenant': tenant,
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_edit_when_not_200(self):
        self.session.put.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.edit,
            tenant_uuid=s.tenant,
            phonebook_body={},
            token=s.token,
        )

    def test_delete(self):
        self.session.delete.return_value = self.new_response(204)
        phonebook_uuid, tenant = 'my_phonebook_uuid', 'zetenant'

        result = self.command.delete(
            tenant_uuid=tenant, phonebook_uuid=phonebook_uuid, token=s.token
        )

        url = f'{self.base_url}/{phonebook_uuid}'
        self.session.delete.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Accent-Tenant': tenant,
            },
        )
        assert_that(result, none())

    def test_delete_when_not_204(self):
        self.session.delete.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.delete,
            token=s.token,
            tenant_uuid=s.tenant,
            phonebook_uuid=s.phonebook_uuid,
        )

    def _assert_get(self, url, token, tenant=None):
        headers = {
            'X-Auth-Token': token,
            'Accept': 'application/json',
        }
        if tenant:
            headers['Accent-Tenant'] = tenant
        self.session.get.assert_called_once_with(url, params={}, headers=headers)
