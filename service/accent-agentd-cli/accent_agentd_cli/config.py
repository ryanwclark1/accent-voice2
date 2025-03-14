# Copyright 2023 Accent Communications

import argparse

from accent.chain_map import ChainMap
from accent.config_helper import parse_config_file, read_config_file_hierarchy

_DEFAULT_CONFIG = {
    'config_file': '/etc/accent-agentd-cli/config.yml',
    'extra_config_files': '/etc/accent-agentd-cli/conf.d',
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/accent-auth-keys/accent-agentd-cli-key.yml',
    },
    'agentd': {
        'host': 'localhost',
        'port': 9493,
        'prefix': None,
        'https': False,
    },
}


def load(argv):
    cli_config = _parse_cli_args(argv)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    key_config = _load_key_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(cli_config, key_config, file_config, _DEFAULT_CONFIG)


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', action='store', help='Command to run.')
    parser.add_argument(
        '--config-file', action='store', help="The path where is the config file."
    )
    parser.add_argument(
        '--host', action='store', help='Hostname of the accent-agentd server.'
    )
    parser.add_argument(
        '--port',
        action='store',
        type=int,
        help='Port number of the accent-agentd server.',
    )
    parsed_args = parser.parse_args(argv)

    result = {'agentd': {}}
    if parsed_args.command:
        result['command'] = parsed_args.command
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.host:
        result['agentd']['host'] = parsed_args.host
    if parsed_args.port:
        result['agentd']['port'] = parsed_args.port

    return result


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    return {
        'auth': {
            'service_id': key_file['service_id'],
            'service_key': key_file['service_key'],
        }
    }
