# Copyright 2023 Accent Communications

import textwrap
import unittest
from unittest.mock import Mock, patch

from accent_confgend.generators.tests.util import assert_config_equal

from ..provd_conf import ProvdNetworkConfGenerator


class TestProvdNetworkConf(unittest.TestCase):
    def setUp(self):
        dependencies = {'config': {}}
        self.generator = ProvdNetworkConfGenerator(dependencies)

    @patch('accent_confgend.plugins.provd_conf.session_scope')
    def test_net4_ip_in_provisioning(self, session_scope):
        session_scope.__enter__ = Mock(return_value=Mock())
        session_scope.__exit__ = Mock(return_value=None)

        with patch.object(
            self.generator, 'get_provd_net4_ip'
        ) as provd_net4_ip, patch.object(
            self.generator, 'get_provd_http_port'
        ) as provd_http_port, patch.object(
            self.generator, 'get_netiface_net4_ip'
        ) as netiface_net4_ip, patch.object(
            self.generator, 'get_provd_http_base_url'
        ) as provd_http_base_url:
            provd_net4_ip.return_value = '10.0.0.254'
            provd_http_base_url.return_value = None
            provd_http_port.return_value = None
            netiface_net4_ip.return_value = None

            value = self.generator.generate()

        assert_config_equal(
            value,
            textwrap.dedent(
                '''\
            general:
                advertised_http_url: http://10.0.0.254
        '''
            ),
        )

    @patch('accent_confgend.plugins.provd_conf.session_scope')
    def test_net4_ip_in_netiface(self, session_scope):
        session_scope.__enter__ = Mock(return_value=Mock())
        session_scope.__exit__ = Mock(return_value=None)

        with patch.object(
            self.generator, 'get_provd_net4_ip'
        ) as provd_net4_ip, patch.object(
            self.generator, 'get_netiface_net4_ip'
        ) as netiface_net4_ip, patch.object(
            self.generator, 'get_provd_http_port'
        ) as provd_http_port, patch.object(
            self.generator, 'get_provd_http_base_url'
        ) as provd_http_base_url:
            provd_net4_ip.return_value = None
            provd_http_base_url.return_value = None
            provd_http_port.return_value = None
            netiface_net4_ip.return_value = '10.0.0.250'

            value = self.generator.generate()

        assert_config_equal(
            value,
            textwrap.dedent(
                '''\
            general:
                advertised_http_url: http://10.0.0.250
        '''
            ),
        )

    @patch('accent_confgend.plugins.provd_conf.session_scope')
    def test_get_provd_http_base_url(self, session_scope):
        session_scope.__enter__ = Mock(return_value=Mock())
        session_scope.__exit__ = Mock(return_value=None)

        with patch.object(
            self.generator, 'get_provd_net4_ip'
        ) as provd_net4_ip, patch.object(
            self.generator, 'get_netiface_net4_ip'
        ) as netiface_net4_ip, patch.object(
            self.generator, 'get_provd_http_port'
        ) as provd_http_port, patch.object(
            self.generator, 'get_provd_http_base_url'
        ) as provd_http_base_url:
            provd_net4_ip.return_value = None
            provd_http_base_url.return_value = 'https://10.0.0.242/custom'
            provd_http_port.return_value = None
            netiface_net4_ip.return_value = None

            value = self.generator.generate()

        assert_config_equal(
            value,
            textwrap.dedent(
                '''\
            general:
                advertised_http_url: https://10.0.0.242/custom
        '''
            ),
        )

    @patch('accent_confgend.plugins.provd_conf.session_scope')
    def test_no_http_base_url(self, session_scope):
        session_scope.__enter__ = Mock(return_value=Mock())
        session_scope.__exit__ = Mock(return_value=None)

        with patch.object(
            self.generator, 'get_provd_net4_ip'
        ) as provd_net4_ip, patch.object(
            self.generator, 'get_netiface_net4_ip'
        ) as netiface_net4_ip, patch.object(
            self.generator, 'get_provd_http_port'
        ) as provd_http_port, patch.object(
            self.generator, 'get_provd_http_base_url'
        ) as provd_http_base_url:
            provd_net4_ip.return_value = '10.0.0.254'
            provd_http_base_url.return_value = None
            provd_http_port.return_value = 8666
            netiface_net4_ip.return_value = '10.0.0.222'

            value = self.generator.generate()

        assert_config_equal(
            value,
            textwrap.dedent(
                '''\
            general:
                advertised_http_url: http://10.0.0.254:8666
        '''
            ),
        )

    @patch('accent_confgend.plugins.provd_conf.session_scope')
    def test_no_advertised_host(self, session_scope):
        session_scope.__enter__ = Mock(return_value=Mock())
        session_scope.__exit__ = Mock(return_value=None)

        with patch.object(
            self.generator, 'get_provd_net4_ip'
        ) as provd_net4_ip, patch.object(
            self.generator, 'get_provd_http_port'
        ) as provd_http_port, patch.object(
            self.generator, 'get_netiface_net4_ip'
        ) as netiface_net4_ip, patch.object(
            self.generator, 'get_provd_http_base_url'
        ) as provd_http_base_url:
            provd_net4_ip.return_value = None
            provd_http_base_url.return_value = None
            provd_http_port.return_value = None
            netiface_net4_ip.return_value = None

            value = self.generator.generate()

        assert_config_equal(value, '{}')
