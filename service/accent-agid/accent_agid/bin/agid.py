# Copyright 2023 Accent Communications

from __future__ import annotations

import argparse
import logging

import accent_dao
from accent.accent_logging import setup_logging, silence_loggers
from accent.chain_map import ChainMap
from accent.config_helper import parse_config_file, read_config_file_hierarchy
from accent.token_renewer import TokenRenewer
from accent.user_rights import change_user
from accent_agentd_client import Client as AgentdClient
from accent_auth_client import Client as AuthClient
from accent_calld_client import Client as CalldClient
from accent_confd_client import Client as ConfdClient
from accent_dird_client import Client as DirdClient

from accent_agid import agid
from accent_agid.modules import *  # noqa

_DEFAULT_CONFIG = {
    'agentd': {
        'host': 'localhost',
        'port': 9493,
        'prefix': None,
        'https': False,
    },
    'dird': {
        'host': 'localhost',
        'port': 9489,
        'prefix': None,
        'https': False,
        'timeout': 1,
    },
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/accent-auth-keys/accent-agid-key.yml',
    },
    'calld': {
        'host': 'localhost',
        'port': 9500,
        'prefix': None,
        'https': False,
    },
    'confd': {
        'host': 'localhost',
        'port': 9486,
        'prefix': None,
        'https': False,
    },
    'user': 'accent-agid',
    'debug': False,
    'logfile': '/var/log/accent-agid.log',
    'listen_port': 4573,
    'listen_address': '127.0.0.1',
    'config_file': '/etc/accent-agid/config.yml',
    'extra_config_files': '/etc/accent-agid/conf.d/',
    'connection_pool_size': 10,
    'db_uri': 'postgresql://asterisk:password123@localhost/asterisk?application_name=accent-agid',
    'call_recording': {
        'filename_template': 'user-{{ srcnum }}-{{ dstnum }}-{{ timestamp }}',
        'filename_extension': 'wav',
    },
}


def main():
    cli_config = _parse_args()
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    key_config = _load_key_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    config = ChainMap(cli_config, key_config, file_config, _DEFAULT_CONFIG)

    setup_logging(config['logfile'], debug=config['debug'])
    silence_loggers(['urllib3'], logging.WARNING)

    user = config.get('user')
    if user:
        change_user(user)

    accent_dao.init_db_from_config(config)

    token_renewer = TokenRenewer(AuthClient(**config['auth']))
    config['agentd']['client'] = AgentdClient(**config['agentd'])
    config['calld']['client'] = CalldClient(**config['calld'])
    config['confd']['client'] = ConfdClient(**config['confd'])
    config['dird']['client'] = DirdClient(**config['dird'])
    config['auth']['client'] = AuthClient(**config['auth'])

    def on_token_change(token_id):
        config['agentd']['client'].set_token(token_id)
        config['calld']['client'].set_token(token_id)
        config['confd']['client'].set_token(token_id)
        config['dird']['client'].set_token(token_id)
        config['auth']['client'].set_token(token_id)

    token_renewer.subscribe_to_token_change(on_token_change)

    agid.init(config)
    with token_renewer:
        agid.run()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config-file', action='store', help='The path to the config file'
    )
    parser.add_argument(
        '-d', action='store_true', dest='debug', help='increase verbosity'
    )
    parser.add_argument('-u', '--user', action='store', help='User to run the daemon')

    parsed_args = parser.parse_args()

    config = {}
    if parsed_args.config_file:
        config['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        config['debug'] = parsed_args.debug
    if parsed_args.user:
        config['user'] = parsed_args.user

    return config


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


if __name__ == '__main__':
    main()
