# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock, patch

from accent_dao.alchemy.moh import MOH
from jinja2.loaders import PackageLoader

from accent_confgend.generators.tests.util import assert_config_equal
from accent_confgend.template import TemplateHelper

from ..musiconhold_conf import MOHConfGenerator


class TestConfBridgeConf(unittest.TestCase):
    def setUp(self):
        self.moh_dao = Mock()
        loader = PackageLoader('accent_confgend.template', 'templates')
        tpl_helper = TemplateHelper(loader)
        dependencies = {'tpl_helper': tpl_helper}
        self.generator = MOHConfGenerator(dependencies)

    @patch('accent_confgend.plugins.musiconhold_conf.moh_dao')
    def test_generate_mode_files(self, mock_moh_dao):
        moh_list = [
            MOH(name='foo', mode='files', sort='alphabetical'),
        ]
        mock_moh_dao.find_all_by.return_value = moh_list

        value = self.generator.generate()

        assert_config_equal(
            value,
            '''
            [default]
            mode = files
            directory = /var/lib/asterisk/moh/default

            [foo]
            mode = files
            directory = /var/lib/asterisk/moh/foo
            sort = alpha
        ''',
        )

    @patch('accent_confgend.plugins.musiconhold_conf.moh_dao')
    def test_generate_mode_custom(self, mock_moh_dao):
        moh_list = [
            MOH(name='bar', mode='custom', application='/bin/false rrr'),
        ]
        mock_moh_dao.find_all_by.return_value = moh_list

        value = self.generator.generate()

        assert_config_equal(
            value,
            '''
            [default]
            mode = files
            directory = /var/lib/asterisk/moh/default

            [bar]
            mode = custom
            application = /bin/false rrr
        ''',
        )

    @patch('accent_confgend.plugins.musiconhold_conf.moh_dao')
    def test_generate_unknown_sort(self, mock_moh_dao):
        moh_list = [
            MOH(name='foo', mode='files', sort='rabbit'),
        ]
        mock_moh_dao.find_all_by.return_value = moh_list

        value = self.generator.generate()

        assert_config_equal(
            value,
            '''
            [default]
            mode = files
            directory = /var/lib/asterisk/moh/default

            [foo]
            mode = files
            directory = /var/lib/asterisk/moh/foo
            sort = rabbit
        ''',
        )
