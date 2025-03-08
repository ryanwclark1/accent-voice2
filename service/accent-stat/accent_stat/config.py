# Copyright 2020-2023 Accent Communications

from accent.chain_map import ChainMap
from accent.config_helper import parse_config_file, read_config_file_hierarchy

_DEFAULT_CONFIG = {
    'config_file': '/etc/accent-stat/config.yml',
    'extra_config_files': '/etc/accent-stat/conf.d',
    'log_filename': '/var/log/accent-stat.log',
    'debug': False,
    'db_uri': 'postgresql://asterisk:password123@localhost/asterisk?application_name=accent-stat',
    'confd': {'host': 'localhost', 'port': 9486, 'prefix': None, 'https': False},
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/accent-auth-keys/accent-stat-key.yml',
    },
}


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    if not key_file:
        return {}
    return {
        'auth': {
            'username': key_file['service_id'],
            'password': key_file['service_key'],
        }
    }


def get_config():
    file_config = read_config_file_hierarchy(_DEFAULT_CONFIG)
    service_key = _load_key_file(ChainMap(file_config, _DEFAULT_CONFIG))
    return ChainMap(service_key, file_config, _DEFAULT_CONFIG)
