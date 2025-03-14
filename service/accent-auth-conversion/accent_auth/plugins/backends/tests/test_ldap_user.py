# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock, call, patch

import ldap
from hamcrest import assert_that, equal_to, has_entries, has_items

from accent_auth.plugins.backends.ldap_user import LDAPUser, _AccentLDAP

ALICE_PAYLOAD = {
    'uuid': 'alice-uuid',
    'emails': [{'address': 'foo@example.com'}],
    'authentication_method': 'ldap',
}


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.user_service = Mock()
        self.user_service.list_users = Mock()
        self.user_service.list_users.return_value = [
            {
                'uuid': 'alice-uuid',
                'purpose': 'user',
                'authentication_method': 'ldap',
            }
        ]
        self.user_service.get_acl = Mock()
        self.user_service.get_acl.return_value = ['acl1']
        self.user_service.get_user_uuid_by_login = Mock()
        self.user_service.get_user_uuid_by_login.return_value = 'alice-uuid'

        self.group_service = Mock()
        self.group_service.get_acl = Mock()
        self.group_service.get_acl.return_value = ['acl2']

        self.ldap_service = Mock()
        self.ldap_service.get = Mock()
        self.ldap_service.get.return_value = {
            'protocol_security': '',
            'protocol_version': 3,
            'port': 389,
            'host': 'host',
            'user_base_dn': 'dc=example,dc=com',
            'user_login_attribute': 'uid',
            'user_email_attribute': 'mail',
        }

        self.tenant_service = Mock()
        self.tenant_service.get_by_uuid_or_slug = Mock()
        self.tenant_service.get_by_uuid_or_slug.return_value = {
            'uuid': 'tenant-uuid-1234',
        }
        self.tenant_service.list_.return_value = [
            {
                'uuid': 'tenant-uuid-1234',
                'domain_names': [
                    'accentvoice.io',
                    'shopify.ca',
                    'mail.accentvoice.io',
                    'stackoverflow.com',
                ],
                'name': '1234',
                'default_authentication_method': 'ldap',
            }
        ]
        self.tenant_service.get.return_value = {
            'default_authentication_method': 'ldap',
        }

        user_metadata_plugin = Mock()
        user_metadata_plugin.get_token_metadata = Mock()
        user_metadata_plugin.get_token_metadata.return_value = {
            'auth_id': 'alice-uuid',
            'pbx_user_uuid': 'alice-uuid',
        }
        user_purpose = Mock()
        user_purpose.metadata_plugins = [user_metadata_plugin]
        self.purposes = {'user': user_purpose}


class TestGetACLS(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.args = {
            'pbx_user_uuid': 'alice-uuid',
            'user_email': 'alice@accent-auth.com',
            'acl': ['acl0'],
        }
        self.backend = LDAPUser()
        self.backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )

    def test_get_acl(self):
        result = self.backend.get_acl('alice', self.args)
        assert_that(result, has_items('acl1', 'acl2'))

    def test_get_acl_when_acls_in_backend(self):
        self.args['acl'] = ['acl0']
        result = self.backend.get_acl('alice', self.args)
        assert_that(result, has_items('acl0', 'acl1', 'acl2'))


class TestGetMetadata(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.args = {'pbx_user_uuid': 'alice-uuid', 'user_email': 'alice@accent-auth.com'}
        self.backend = LDAPUser()
        self.backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            },
        )

    def test_that_get_metadata_calls_the_dao(self):
        expected_result = has_entries(
            auth_id='alice-uuid',
            pbx_user_uuid='alice-uuid',
        )
        result = self.backend.get_metadata('alice', self.args)
        assert_that(result, expected_result)

    def test_that_get_metadata_raises_if_no_user(self):
        self.assertRaises(Exception, self.backend.get_metadata, 'alice', None)


@patch('accent_auth.plugins.backends.ldap_user._AccentLDAP')
class TestVerifyPassword(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.expected_user_dn = 'uid=foo,dc=example,dc=com'
        self.expected_user_email = 'foo@example.com'
        obj = {'mail': self.expected_user_email.encode('utf-8')}
        self.search_obj_result = (self.expected_user_dn, obj)
        self.list_users = Mock()
        self.user_service = Mock(list_users=self.list_users)

    def test_that_verify_password_return_false_when_ldaperror(self, accent_ldap):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )
        accent_ldap = accent_ldap.return_value
        accent_ldap.connect.side_effect = ldap.LDAPError
        args = {'tenant_id': 'test'}

        result = backend.verify_password('foo', 'bar', args)
        assert_that(result, equal_to(False))

    def test_that_verify_password_return_false_when_serverdown(self, accent_ldap):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            },
        )
        accent_ldap = accent_ldap.return_value
        accent_ldap.uri = 'host'
        accent_ldap.connect.side_effect = ldap.SERVER_DOWN
        args = {'tenant_id': 'test'}

        result = backend.verify_password('foo', 'bar', args)
        assert_that(result, equal_to(False))

    def test_that_verify_password_calls_perform_bind(self, accent_ldap):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )

        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = self.search_obj_result
        self.list_users.return_value = [ALICE_PAYLOAD]
        args = {'tenant_id': 'test'}

        result = backend.verify_password('foo', 'bar', args)

        assert_that(result, equal_to(True))
        accent_ldap.perform_bind.assert_called_once_with(self.expected_user_dn, 'bar')

    def test_that_verify_password_escape_dn_chars(self, accent_ldap):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )

        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = (
            'uid=fo\\+o,dc=example,dc=com',
            {'mail': self.expected_user_email.encode('utf-8')},
        )
        self.list_users.return_value = [ALICE_PAYLOAD]
        args = {'tenant_id': 'test'}

        result = backend.verify_password('fo+o', 'bar', args)

        assert_that(result, equal_to(True))
        accent_ldap.perform_bind.assert_called_once_with(
            'uid=fo\\+o,dc=example,dc=com', 'bar'
        )

    def test_that_verify_password_escape_filter_chars(self, accent_ldap):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )

        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = (
            'uid=fo\\+o,dc=example,dc=com',
            {'mail': self.expected_user_email.encode('utf-8')},
        )
        self.list_users.return_value = [ALICE_PAYLOAD]
        args = {'tenant_id': 'test'}

        result = backend.verify_password('fo+o', 'bar', args)

        assert_that(result, equal_to(True))
        accent_ldap.perform_search.assert_called_once_with(
            'uid=fo\\+o,dc=example,dc=com', 0, attrlist=['mail']
        )

    def test_that_verify_password_calls_return_false_when_no_user_bind(self, accent_ldap):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )
        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = False
        args = {'tenant_id': 'test'}

        result = backend.verify_password('foo', 'bar', args)

        assert_that(result, equal_to(False))
        accent_ldap.perform_bind.assert_called_once_with(self.expected_user_dn, 'bar')

    def test_that_verify_password_calls_return_False_when_no_email_associated(
        self, accent_ldap
    ):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )
        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = self.search_obj_result
        self.list_users.return_value = []
        args = {'tenant_id': 'test'}

        result = backend.verify_password('foo', 'bar', args)

        assert_that(result, equal_to(False))
        assert_that(args, equal_to({'tenant_id': 'test'}))

    def test_that_verify_password_calls_with_bind_dn(self, accent_ldap):
        self.ldap_service.get.return_value.update(
            {'bind_dn': 'uid=foo,dc=example,dc=com', 'bind_password': 'S3cr$t'}
        )
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )
        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = self.search_obj_result
        self.list_users.return_value = [ALICE_PAYLOAD]
        args = {'tenant_id': 'test'}

        result = backend.verify_password('foo', 'bar', args)

        assert_that(result, equal_to(True))
        assert_that(
            args,
            equal_to(
                {
                    'tenant_id': 'test',
                    'pbx_user_uuid': 'alice-uuid',
                    'user_email': 'foo@example.com',
                    'real_login': 'foo@example.com',
                }
            ),
        )
        expected_call = [
            call('uid=foo,dc=example,dc=com', 'S3cr$t'),
            call(self.expected_user_dn, 'bar'),
        ]
        accent_ldap.perform_bind.assert_has_calls(expected_call)

    def test_that_verify_password_calls_with_missing_bind_password_try_bind(
        self, accent_ldap
    ):
        self.ldap_service.get.return_value.update(
            {'bind_dn': 'uid=foo,dc=example,dc=com'}
        )
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )
        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = self.search_obj_result
        self.list_users.return_value = [ALICE_PAYLOAD]
        args = {'tenant_id': 'test'}

        result = backend.verify_password('foo', 'bar', args)

        assert_that(result, equal_to(True))
        assert_that(
            args,
            equal_to(
                {
                    'tenant_id': 'test',
                    'pbx_user_uuid': 'alice-uuid',
                    'user_email': 'foo@example.com',
                    'real_login': 'foo@example.com',
                }
            ),
        )
        accent_ldap.perform_bind.assert_called_once_with(self.expected_user_dn, 'bar')

    def test_that_verify_password_works_using_domain_name(self, accent_ldap):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )

        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = self.search_obj_result
        self.list_users.return_value = [ALICE_PAYLOAD]
        args = {'domain_name': 'accentvoice.io'}

        result = backend.verify_password('foo', 'bar', args)

        assert_that(result, equal_to(True))

    def test_that_verify_password_works_using_case_sensitive_email_address(
        self, accent_ldap
    ):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )

        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = self.search_obj_result
        self.list_users.return_value = [ALICE_PAYLOAD]
        args = {'domain_name': 'accentvoice.io'}

        result = backend.verify_password('FoO@EXampLE.coM', 'bar', args)

        assert_that(result, equal_to(True))

    def test_that_verify_password_using_non_existing_domain_name_returns_false(
        self, accent_ldap
    ):
        backend = LDAPUser()
        backend.load(
            {
                'user_service': self.user_service,
                'group_service': self.group_service,
                'ldap_service': self.ldap_service,
                'tenant_service': self.tenant_service,
                'purposes': self.purposes,
            }
        )

        accent_ldap = accent_ldap.return_value
        accent_ldap.perform_bind.return_value = True
        accent_ldap.perform_search.return_value = self.search_obj_result
        self.list_users.return_value = [{'uuid': 'alice-uuid'}]
        self.tenant_service.list_.return_value = []
        args = {'domain_name': 'gmail.com'}

        result = backend.verify_password('foo', 'bar', args)

        assert_that(result, equal_to(False))


class TestAccentLDAP(unittest.TestCase):
    def setUp(self):
        self.config = {
            'protocol_security': '',
            'protocol_version': 3,
            'port': 389,
            'host': 'host',
            'user_base_dn': 'dc=example,dc=com',
            'user_login_attribute': 'uid',
        }

    @patch('ldap.initialize')
    def test_accent_ldap_init(self, ldap_initialize):
        ldapobj = ldap_initialize.return_value = Mock()

        accent_ldap = _AccentLDAP(self.config)
        accent_ldap.connect()

        ldap_initialize.assert_called_once_with(accent_ldap.uri)
        ldapobj.set_option.assert_any_call(ldap.OPT_REFERRALS, 0)
        ldapobj.set_option.assert_any_call(ldap.OPT_NETWORK_TIMEOUT, 2)
        ldapobj.set_option.assert_any_call(ldap.OPT_TIMEOUT, 2)
        ldapobj.set_option.assert_any_call(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)

    @patch('ldap.initialize')
    def test_accent_ldap_init_tls(self, ldap_initialize):
        ldapobj = ldap_initialize.return_value = Mock()

        with patch.dict(self.config, {'protocol_security': 'tls'}):
            accent_ldap = _AccentLDAP(self.config)
            accent_ldap.connect()

        ldap_initialize.assert_called_once_with(accent_ldap.uri)
        ldapobj.set_option.assert_any_call(ldap.OPT_REFERRALS, 0)
        ldapobj.set_option.assert_any_call(ldap.OPT_NETWORK_TIMEOUT, 2)
        ldapobj.set_option.assert_any_call(ldap.OPT_TIMEOUT, 2)
        ldapobj.set_option.assert_any_call(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
        ldapobj.set_option.assert_any_call(ldap.OPT_X_TLS_NEWCTX, 0)
        ldapobj.start_tls_s.assert_called_once()

    @patch('ldap.initialize', Mock())
    def test_that_perform_bind(self):
        accent_ldap = _AccentLDAP(self.config)
        accent_ldap.connect()

        result = accent_ldap.perform_bind('username', 'password')
        self.assertEqual(result, True)

    @patch('ldap.initialize')
    def test_that_perform_bind_return_false_when_no_wrong_credential(
        self, ldap_initialize
    ):
        ldapobj = ldap_initialize.return_value = Mock()

        accent_ldap = _AccentLDAP(self.config)
        accent_ldap.connect()
        ldapobj.simple_bind_s.side_effect = ldap.INVALID_CREDENTIALS()
        result = accent_ldap.perform_bind('username', 'password')
        self.assertEqual(result, False)

    @patch('ldap.initialize')
    def test_that_perform_search(self, ldap_initialize):
        ldapobj = ldap_initialize.return_value = Mock()
        accent_ldap = _AccentLDAP(self.config)
        accent_ldap.connect()
        ldapobj.search_ext_s.return_value = ['result1']

        result = accent_ldap.perform_search('base', 'scope')
        self.assertEqual(result, 'result1')

    @patch('ldap.initialize')
    def test_that_perform_search_return_none_when_multiple_result(
        self, ldap_initialize
    ):
        ldapobj = ldap_initialize.return_value = Mock()
        accent_ldap = _AccentLDAP(self.config)
        accent_ldap.connect()
        ldapobj.search_ext_s.side_effect = ldap.SIZELIMIT_EXCEEDED()

        result_dn, result_attr = accent_ldap.perform_search('base', 'scope')
        self.assertEqual(result_dn, None)
        self.assertEqual(result_attr, None)

    @patch('ldap.initialize')
    def test_that_perform_search_return_none_when_no_result(self, ldap_initialize):
        ldapobj = ldap_initialize.return_value = Mock()
        accent_ldap = _AccentLDAP(self.config)
        accent_ldap.connect()
        ldapobj.search_ext_s.return_value = []

        result_dn, result_attr = accent_ldap.perform_search('base', 'scope')
        self.assertEqual(result_dn, None)
        self.assertEqual(result_attr, None)
