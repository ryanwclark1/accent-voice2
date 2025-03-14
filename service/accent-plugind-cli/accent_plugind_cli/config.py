# Copyright 2023 Accent Communications

import argparse

from accent.chain_map import ChainMap
from accent.config_helper import parse_config_file

_DEFAULT_CONFIG = {
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/accent-auth-keys/accent-plugind-cli-key.yml',
    },
    'plugind': {
        'host': 'localhost',
        'port': 9503,
        'prefix': None,
        'https': False,
    },
    'bus': {
        'username': 'guest',
        'password': 'guest',
        'host': 'localhost',
        'port': 5672,
        'exchange_name': 'accent-headers',
        'exchange_type': 'headers',
    },
}


def load_config(argv):
    cli_config = _parse_cli_args(argv)
    key_config = _load_key_file(ChainMap(cli_config, _DEFAULT_CONFIG))
    return ChainMap(cli_config, key_config, _DEFAULT_CONFIG)


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', action='store', help='Command to run.')
    parsed_args = parser.parse_args(argv)
    result = {}
    if parsed_args.command:
        result['command'] = parsed_args.command

    return result


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    return {
        'auth': {
            'service_id': key_file['service_id'],
            'service_key': key_file['service_key'],
        }
    }
