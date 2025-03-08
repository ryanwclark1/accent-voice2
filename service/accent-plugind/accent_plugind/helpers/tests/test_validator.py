# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import ANY, Mock, patch

from accent_test_helpers.hamcrest.raises import raises
from hamcrest import assert_that, calling, has_properties, not_

from accent_plugind import exceptions
from accent_plugind.config import _MAX_PLUGIN_FORMAT_VERSION

from ..validator import Validator

CURRENT_ACCENT_VERSION = '17.10'


class TestValidator(TestCase):
    def setUp(self):
        self.plugin_db = Mock()

    def test_that_missing_fields_raises(self):
        validator = self.new_validator()

        metadata = self.new_metadata()
        metadata.pop('version', None)

        expected_details = {
            'version': {
                'constraint_id': 'required',
                'constraint': 'required',
                'message': ANY,
            }
        }
        assert_that(
            calling(validator.validate).with_args(metadata),
            raises(exceptions.PluginValidationException).matching(
                has_properties(
                    'error_id',
                    'validation-error',
                    'message',
                    'Validation error',
                    'details',
                    expected_details,
                )
            ),
        )

    def test_that_invalid_name_raises(self):
        validator = self.new_validator()

        metadata = self.new_metadata(name='no_underscore_allowed')

        expected_details = {'name': {'constraint_id': 'regex', 'constraint': ANY, 'message': ANY}}
        assert_that(
            calling(validator.validate).with_args(metadata),
            raises(exceptions.PluginValidationException).matching(
                has_properties(
                    'error_id',
                    'validation-error',
                    'message',
                    'Validation error',
                    'details',
                    expected_details,
                )
            ),
        )

    def test_that_invalid_namespace_raises(self):
        validator = self.new_validator()

        metadata = self.new_metadata(namespace='no-dash-allowed')

        expected_details = {'namespace': {'constraint_id': 'regex', 'constraint': ANY, 'message': ANY}}
        assert_that(
            calling(validator.validate).with_args(metadata),
            raises(exceptions.PluginValidationException).matching(
                has_properties(
                    'error_id',
                    'validation-error',
                    'message',
                    'Validation error',
                    'details',
                    expected_details,
                )
            ),
        )

    def test_plugin_format_version_from_the_future(self):
        validator = self.new_validator()

        metadata = self.new_metadata(plugin_format_version=_MAX_PLUGIN_FORMAT_VERSION + 1)

        expected_details = {
            'plugin_format_version': {
                'constraint_id': 'range',
                'constraint': {'min': 0, 'max': _MAX_PLUGIN_FORMAT_VERSION},
                'message': ANY,
            }
        }
        assert_that(
            calling(validator.validate).with_args(metadata),
            raises(exceptions.PluginValidationException).matching(
                has_properties(
                    'error_id',
                    'validation-error',
                    'message',
                    'Validation error',
                    'details',
                    expected_details,
                )
            ),
        )

    def test_max_accent_version_too_small(self):
        validator = self.new_validator()

        metadata = self.new_metadata(max_accent_version='16.16')

        expected_details = {
            'max_accent_version': {
                'constraint_id': 'range',
                'constraint': {'min': CURRENT_ACCENT_VERSION},
                'message': ANY,
            }
        }
        assert_that(
            calling(validator.validate).with_args(metadata),
            raises(exceptions.PluginValidationException).matching(
                has_properties(
                    'error_id',
                    'validation-error',
                    'message',
                    'Validation error',
                    'details',
                    expected_details,
                )
            ),
        )

    def test_min_accent_version_too_high(self):
        validator = self.new_validator()

        metadata = self.new_metadata(min_accent_version='17.11')

        expected_details = {
            'min_accent_version': {
                'constraint_id': 'range',
                'constraint': {'max': CURRENT_ACCENT_VERSION},
                'message': ANY,
            }
        }
        assert_that(
            calling(validator.validate).with_args(metadata),
            raises(exceptions.PluginValidationException).matching(
                has_properties(
                    'error_id',
                    'validation-error',
                    'message',
                    'Validation error',
                    'details',
                    expected_details,
                )
            ),
        )

    def test_plugin_already_installed(self):
        validator = self.new_validator()
        metadata = self.new_metadata()
        with patch.object(validator._db, 'is_installed', return_value=True):
            assert_that(
                calling(validator.validate).with_args(metadata),
                raises(exceptions.PluginAlreadyInstalled),
            )

        validator = self.new_validator(install_params={'reinstall': True})
        metadata = self.new_metadata()
        with patch.object(validator._db, 'is_installed', return_value=True):
            assert_that(
                calling(validator.validate).with_args(metadata),
                not_(raises(exceptions.PluginAlreadyInstalled)),
            )

    def new_metadata(self, name='valid-name', namespace='validns', version='0.0.1', **kwargs):
        metadata = dict(kwargs)
        metadata['name'] = name
        metadata['namespace'] = namespace
        metadata['version'] = version
        return metadata

    def new_validator(self, plugin_db=None, accent_version=CURRENT_ACCENT_VERSION, install_params=None):
        plugin_db = plugin_db or self.plugin_db
        install_params = install_params or {'reinstall': False}
        return Validator(plugin_db, accent_version, install_params)
