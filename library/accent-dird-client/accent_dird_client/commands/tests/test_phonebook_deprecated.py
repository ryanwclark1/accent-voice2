# Copyright 2023 Accent Communications

from unittest.mock import sentinel as s

from hamcrest import assert_that, equal_to, none
from accent_lib_rest_client.tests.command import RESTCommandTestCase

from ..phonebook_deprecated import DeprecatedPhonebookCommand


class TestPhonebookContactDeprecated(RESTCommandTestCase):
    Command = DeprecatedPhonebookCommand

    def setUp(self):
        super().setUp()
        self.tenant = 'atenant'
        self.phonebook_id = 42

    def test_create(self):
        self.session.post.return_value = self.new_response(
            201, json={'return': 'value'}
        )
        contact_body = {'firstname': 'Foo', 'lastname': 'Bar'}

        result = self.command.create_contact(
            tenant=self.tenant,
            phonebook_id=self.phonebook_id,
            token=s.token,
            contact_body=contact_body,
        )

        url = f'{self.base_url}/{self.tenant}/phonebooks/{self.phonebook_id}/contacts'
        self.session.post.assert_called_once_with(
            url,
            json=contact_body,
            params={},
            headers={
                'Accept': 'application/json',
                'X-Auth-Token': s.token,
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_create_when_not_201(self):
        self.session.post.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.create, phonebook_body={}, tenant=self.tenant, token=s.token
        )

    def test_list(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.list_contacts(
            tenant=self.tenant, token=s.token, phonebook_id=self.phonebook_id
        )

        url = f'{self.base_url}/{self.tenant}/phonebooks/{self.phonebook_id}/contacts'
        self.session.get.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_list_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.list_contacts,
            token=s.token,
            tenant=self.tenant,
            phonebook_id=self.phonebook_id,
        )

    def test_get(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.get_contact(
            token=s.token,
            tenant=self.tenant,
            phonebook_id=self.phonebook_id,
            contact_uuid=s.contact_uuid,
        )

        url = (
            f'{self.base_url}/{self.tenant}/phonebooks/'
            f'{self.phonebook_id}/contacts/{s.contact_uuid}'
        )
        self.session.get.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_get_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.get_contact,
            token=s.token,
            tenant=self.tenant,
            phonebook_id=self.phonebook_id,
            contact_uuid=s.contact_uuid,
        )

    def test_edit(self):
        self.session.put.return_value = self.new_response(200, json={'return': 'value'})
        body = {'firstname': 'test'}

        result = self.command.edit_contact(
            tenant=self.tenant,
            phonebook_id=self.phonebook_id,
            contact_uuid=s.contact_uuid,
            contact_body=body,
            token=s.token,
        )

        url = (
            f'{self.base_url}/{self.tenant}/phonebooks/'
            f'{self.phonebook_id}/contacts/{s.contact_uuid}'
        )

        self.session.put.assert_called_once_with(
            url,
            json=body,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_edit_when_not_200(self):
        self.session.put.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.edit_contact)

    def test_delete(self):
        self.session.delete.return_value = self.new_response(204)

        result = self.command.delete_contact(
            tenant=self.tenant,
            phonebook_id=self.phonebook_id,
            contact_uuid=s.contact_uuid,
            token=s.token,
        )

        url = (
            f'{self.base_url}/{self.tenant}/phonebooks/'
            f'{self.phonebook_id}/contacts/{s.contact_uuid}'
        )
        self.session.delete.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, none())

    def test_delete_when_not_204(self):
        self.session.delete.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.delete,
            token=s.token,
            tenant=s.tenant,
            phonebook_id=s.phonebook_id,
        )


class TestPhonebook(RESTCommandTestCase):
    Command = DeprecatedPhonebookCommand

    def test_create(self):
        self.session.post.return_value = self.new_response(
            201, json={'return': 'value'}
        )
        phonebook_body = {'name': 'main', 'description': 'The main phonebook'}
        tenant = 'mytenant'

        result = self.command.create(
            tenant=tenant, token=s.token, phonebook_body=phonebook_body
        )

        url = f'{self.base_url}/mytenant/phonebooks'
        self.session.post.assert_called_once_with(
            url,
            json=phonebook_body,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_create_when_not_201(self):
        self.session.post.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.create,
            phonebook_body={'name': 'main'},
            tenant='thetenant',
            token=s.token,
        )

    def test_list_phonebook(self):
        tenant = 'mytenant'
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.list(tenant=tenant, token=s.token)

        url = f'{self.base_url}/mytenant/phonebooks'
        self._assert_get(url=url, token=s.token)
        assert_that(result, equal_to({'return': 'value'}))

    def test_list_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.list, s.token, 'mytenant')

    def test_get(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        tenant, phonebook_id = 'atenant', 42

        result = self.command.get(
            token=s.token, tenant=tenant, phonebook_id=phonebook_id
        )

        url = f'{self.base_url}/{tenant}/phonebooks/{phonebook_id}'
        self._assert_get(url, s.token)
        assert_that(result, equal_to({'return': 'value'}))

    def test_get_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.get,
            token=s.token,
            tenant='mytenant',
            phonebook_id=42,
        )

    def test_edit(self):
        self.session.put.return_value = self.new_response(200, json={'return': 'value'})
        tenant = 'thetenant'
        phonebook_id = 'my_contact_id'
        body = {'name': 'test'}

        result = self.command.edit(
            tenant=tenant, phonebook_id=phonebook_id, phonebook_body=body, token=s.token
        )

        url = f'{self.base_url}/{tenant}/phonebooks/{phonebook_id}'
        self.session.put.assert_called_once_with(
            url,
            json=body,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_edit_when_not_200(self):
        self.session.put.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.edit,
            tenant=s.tenant,
            phonebook_body={},
            token=s.token,
        )

    def test_delete(self):
        self.session.delete.return_value = self.new_response(204)
        phonebook_id, tenant = 'my_phonebook_id', 'zetenant'

        result = self.command.delete(
            tenant=tenant, phonebook_id=phonebook_id, token=s.token
        )

        url = f'{self.base_url}/{tenant}/phonebooks/{phonebook_id}'
        self.session.delete.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, none())

    def test_delete_when_not_204(self):
        self.session.delete.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.delete,
            token=s.token,
            tenant=s.tenant,
            phonebook_id=s.phonebook_id,
        )

    def _assert_get(self, url, token):
        self.session.get.assert_called_once_with(
            url,
            params={},
            headers={
                'X-Auth-Token': token,
                'Accept': 'application/json',
            },
        )
