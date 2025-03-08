# Copyright 2023 Accent Communications


from accent.accent_logging import get_log_level_by_name
from accent.chain_map import ChainMap
from accent.config_helper import read_config_file_hierarchy

_DEFAULT_CONFIG = {
    'config_file': '/etc/accent-confgend/config.yml',
    'extra_config_files': '/etc/accent-confgend/conf.d',
    'debug': False,
    'log_level': 'info',
    'log_filename': '/var/log/accent-confgend.log',
    'cache': '/var/cache/accent-confgend',
    'listen_address': '127.0.0.1',
    'listen_port': 8669,
    'db_uri': 'postgresql://asterisk:password123@localhost/asterisk?application_name=accent-confgend',
    'templates': {'contextsconf': '/etc/accent-confgend/templates/contexts.conf'},
    'plugins': {},
}


def load():
    file_config = read_config_file_hierarchy(_DEFAULT_CONFIG)
    reinterpreted_config = _get_reinterpreted_raw_values(
        ChainMap(file_config, _DEFAULT_CONFIG)
    )
    config = ChainMap(reinterpreted_config, file_config, _DEFAULT_CONFIG)
    return config


def _get_reinterpreted_raw_values(config):
    result = {}

    if config.get('listen_address') == '*':
        result = {'listen_address': ''}

    log_level = config.get('log_level')
    if log_level:
        result['log_level'] = get_log_level_by_name(log_level)

    return result
