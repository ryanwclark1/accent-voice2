# Copyright 2023 Accent Communications

import argparse

from accent.accent_logging import get_log_level_by_name
from accent.chain_map import ChainMap
from accent.config_helper import parse_config_file, read_config_file_hierarchy

_DEFAULT_HTTP_PORT = 9302

_DEFAULT_CONFIG = {
    'config_file': '/etc/accent-setupd/config.yml',
    'debug': False,
    'extra_config_files': '/etc/accent-setupd/conf.d',
    'log_file': '/var/log/accent-setupd.log',
    'log_level': 'info',
    'user': 'accent-setupd',
    'self_stop_delay': 10.0,
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/accent-auth-keys/accent-setupd-key.yml',
        'master_tenant_uuid': None,
    },
    'bus': {
        'username': 'guest',
        'password': 'guest',
        'host': 'localhost',
        'port': 5672,
        'exchange_name': 'accent-headers',
        'exchange_type': 'headers',
    },
    'confd': {'host': 'localhost', 'port': 9486, 'prefix': None, 'https': False},
    'rest_api': {
        'listen': '127.0.0.1',
        'port': _DEFAULT_HTTP_PORT,
        'certificate': None,
        'private_key': None,
        'cors': {'enabled': True, 'allow_headers': ['Content-Type', 'X-Auth-Token']},
    },
    'consul': {
        'scheme': 'http',
        'port': 8500,
    },
    'service_discovery': {
        'enabled': False,
        'advertise_address': 'auto',
        'advertise_address_interface': 'eth0',
        'advertise_port': _DEFAULT_HTTP_PORT,
        'ttl_interval': 30,
        'refresh_interval': 27,
        'retry_interval': 2,
        'extra_tags': [],
    },
    'sysconfd': {'host': 'localhost', 'port': 8668},
    'enabled_plugins': {'api': True, 'config': True, 'setup': True, 'status': True},
}


def load_config(args):
    cli_config = _parse_cli_args(args)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(cli_config, file_config, _DEFAULT_CONFIG)
    service_key = _load_key_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(reinterpreted_config, cli_config, service_key, file_config, _DEFAULT_CONFIG)


def _get_reinterpreted_raw_values(*configs):
    config = ChainMap(*configs)
    return {
        'log_level': get_log_level_by_name('debug' if config['debug'] else config['log_level']),
    }


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    return {
        'auth': {
            'username': key_file['service_id'],
            'password': key_file['service_key'],
        }
    }


def _parse_cli_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', action='store', help='The path to the config file')
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Log debug mesages. Override log_level',
    )
    parser.add_argument('-u', '--user', action='store', help='The owner of the process')
    parsed_args = parser.parse_args()

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
    if parsed_args.user:
        result['user'] = parsed_args.user

    return result
