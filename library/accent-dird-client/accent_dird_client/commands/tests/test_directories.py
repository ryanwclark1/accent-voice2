# Copyright 2023 Accent Communications

from unittest.mock import sentinel as s

from hamcrest import assert_that, equal_to, none
from accent_lib_rest_client.tests.command import RESTCommandTestCase

from ..directories import DirectoriesCommand


class TestDirectories(RESTCommandTestCase):
    Command = DirectoriesCommand

    def test_lookup(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.lookup(profile='default', term='Alice', token=s.token)

        self.session.get.assert_called_once_with(
            f'{self.base_url}/lookup/default',
            params={'term': 'Alice'},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_lookup_when_not_200(self):
        self.session.get.return_value = self.new_response(404)

        self.assertRaisesHTTPError(self.command.lookup, profile='my_profile')

    def test_lookup_user(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.lookup_user(
            profile='default',
            user_uuid='user-uuid',
            term='Alice',
            token=s.token,
        )

        self.session.get.assert_called_once_with(
            f'{self.base_url}/lookup/default/user-uuid',
            params={'term': 'Alice'},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_reverse(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.reverse(
            profile='default', user_uuid='abcd-1234', exten='1234', token=s.token
        )

        self.session.get.assert_called_once_with(
            f'{self.base_url}/reverse/default/abcd-1234',
            params={'exten': '1234'},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_reverse_deprecated_version(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.reverse(
            profile='default', accent_user_uuid='abcd-1234', exten='1234', token=s.token
        )

        self.session.get.assert_called_once_with(
            f'{self.base_url}/reverse/default/abcd-1234',
            params={'exten': '1234'},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_reverse_when_not_200(self):
        self.session.get.return_value = self.new_response(404)

        self.assertRaisesHTTPError(
            self.command.reverse, profile='my_profile', accent_user_uuid='abcd-1234'
        )

    def test_headers(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.headers(profile='default', token=s.token)

        self.session.get.assert_called_once_with(
            f'{self.base_url}/lookup/default/headers',
            params={},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_headers_when_not_200(self):
        self.session.get.return_value = self.new_response(404)

        self.assertRaisesHTTPError(self.command.headers, profile='my_profile')

    def test_favorites(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.favorites(profile='default', token=s.token)

        self.session.get.assert_called_once_with(
            f'{self.base_url}/favorites/default',
            params={},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_favorites_when_not_200(self):
        self.session.get.return_value = self.new_response(404)

        self.assertRaisesHTTPError(self.command.favorites, profile='my_profile')

    def test_new_favorite(self):
        self.session.put.return_value = self.new_response(204)

        result = self.command.new_favorite('my_directory', 'my_contact', token=s.token)

        self.session.put.assert_called_once_with(
            f'{self.base_url}/favorites/my_directory/my_contact',
            params={},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, none())

    def test_new_favorite_when_not_204(self):
        self.session.put.return_value = self.new_response(404)

        self.assertRaisesHTTPError(
            self.command.new_favorite, 'my_directory', 'my_contact'
        )

    def test_remove_favorite(self):
        self.session.delete.return_value = self.new_response(204)

        result = self.command.remove_favorite(
            'my_directory', 'my_contact', token=s.token
        )

        self.session.delete.assert_called_once_with(
            f'{self.base_url}/favorites/my_directory/my_contact',
            params={},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, none())

    def test_remove_favorite_when_not_204(self):
        self.session.delete.return_value = self.new_response(404)

        self.assertRaisesHTTPError(
            self.command.remove_favorite, 'my_directory', 'my_contact'
        )

    def test_personal(self):
        self.session.get.return_value = self.new_response(200, json={'return': 'value'})

        result = self.command.personal(profile='default', token=s.token)

        self.session.get.assert_called_once_with(
            f'{self.base_url}/personal/default',
            params={},
            headers={'X-Auth-Token': s.token, 'Accept': 'application/json'},
        )
        assert_that(result, equal_to({'return': 'value'}))

    def test_personal_when_not_200(self):
        self.session.get.return_value = self.new_response(404)

        self.assertRaisesHTTPError(self.command.personal, profile='my_profile')
