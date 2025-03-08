# Copyright 2023 Accent Communications

from unittest.mock import sentinel as s

from hamcrest import assert_that, equal_to, is_, none
from accent_lib_rest_client.tests.command import RESTCommandTestCase

from ..personal import PersonalCommand


class TestPersonal(RESTCommandTestCase):
    Command = PersonalCommand

    def test_list(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.list(token=s.token)

        self.session.get.assert_called_once_with(
            self.base_url,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_purge(self):
        self.session.delete.return_value = self.new_response(204)

        result = self.command.purge(token=s.token)

        self.session.delete.assert_called_once_with(
            self.base_url,
            params={},
            headers={
                'Accept': 'application/json',
                'X-Auth-Token': s.token,
            },
        )
        assert_that(result, none())

    def test_list_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.list, s.token)

    def test_export_csv(self):
        csv = 'firstname\r\nAlice'
        self.session.get.return_value = self.new_response(200, body=csv)

        result = self.command.export_csv(token=s.token)

        self.session.get.assert_called_once_with(
            self.base_url,
            params={'format': 'text/csv'},
            headers={'X-Auth-Token': s.token},
        )
        assert_that(result, equal_to(csv))

    def test_export_csv_when_empty(self):
        self.session.get.return_value = self.new_response(204)

        result = self.command.export_csv(token=s.token)

        assert_that(result, is_(none()))

    def test_export_csv_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.export_csv, s.token)

    def test_get(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})
        contact_id = 'my_contact_id'

        result = self.command.get(contact_id, token=s.token)

        self.session.get.assert_called_once_with(
            f'{self.base_url}/{contact_id}',
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_get_when_not_200(self):
        self.session.get.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.get, 'my_contact_id', s.token)

    def test_import_csv(self):
        self.session.post.return_value = self.new_response(
            201, json={'return': 'value'}
        )
        csv = 'firstname,lastname\ndaniel,martini'

        result = self.command.import_csv(csv, encoding='cp1252', token=s.token)

        self.session.post.assert_called_once_with(
            f'{self.base_url}/import',
            data=csv,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
                'Content-Type': 'text/csv; charset=cp1252',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_import_csv_when_not_201(self):
        self.session.post.return_value = self.new_response(401)

        self.assertRaisesHTTPError(
            self.command.import_csv, 'firstname,lastname\ndaniel,martini'
        )

    def test_create(self):
        self.session.post.return_value = self.new_response(
            201, json={'return': 'value'}
        )
        contact = {'firstname': 'Alice'}

        result = self.command.create(contact, token=s.token)

        self.session.post.assert_called_once_with(
            self.base_url,
            json=contact,
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_create_when_not_201(self):
        self.session.post.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.create, {'firstname': 'Alice'}, s.token)

    def test_edit(self):
        self.session.put.return_value = self.new_response(200, json={'return': 'value'})
        contact_id = 'my_contact_id'
        contact = {'firstname': 'Alice'}

        result = self.command.edit(contact_id, contact, token=s.token)

        self.session.put.assert_called_once_with(
            f'{self.base_url}/{contact_id}',
            json=contact,
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
            'my_contact_id',
            {'firstname': 'Alice'},
            s.token,
        )

    def test_delete(self):
        self.session.delete.return_value = self.new_response(204)
        contact_id = 'my_contact_id'

        result = self.command.delete(contact_id, token=s.token)

        self.session.delete.assert_called_once_with(
            f'{self.base_url}/{contact_id}',
            params={},
            headers={
                'X-Auth-Token': s.token,
                'Accept': 'application/json',
            },
        )
        assert_that(result, none())

    def test_delete_when_not_201(self):
        self.session.delete.return_value = self.new_response(401)

        self.assertRaisesHTTPError(self.command.delete, {'firstname': 'Alice'}, s.token)
