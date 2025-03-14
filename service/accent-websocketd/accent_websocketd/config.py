# Copyright 2023 Accent Communications

from __future__ import annotations

import argparse
import logging
import ssl
from typing import Any

from accent.accent_logging import get_log_level_by_name
from accent.chain_map import ChainMap
from accent.config_helper import parse_config_file, read_config_file_hierarchy

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG = {
    'config_file': '/etc/accent-websocketd/config.yml',
    'extra_config_files': '/etc/accent-websocketd/conf.d/',
    'debug': False,
    'log_level': 'info',
    'log_file': '/var/log/accent-websocketd.log',
    'user': 'accent-websocketd',
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/accent-auth-keys/accent-websocketd-key.yml',
    },
    'auth_check_strategy': 'dynamic',
    'bus': {
        'host': 'localhost',
        'port': 5672,
        'username': 'guest',
        'password': 'guest',
        'vhost': '',
        'exchange_name': 'accent-headers',
        'exchange_type': 'headers',
        'consumer_prefetch': 250,
    },
    'websocket': {
        'listen': '127.0.0.1',
        'port': 9502,
        'certificate': None,
        'private_key': None,
        'ping_interval': 60,
    },
    'process_workers': 'auto',
    'worker_connections': 1,
}


def load_config():
    cli_config = _parse_cli_args()
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    service_key = _load_key_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(
        ChainMap(cli_config, file_config, _DEFAULT_CONFIG)
    )
    return ChainMap(
        reinterpreted_config, cli_config, service_key, file_config, _DEFAULT_CONFIG
    )


def _parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config-file', action='store', help="The path where is the config file"
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help="Log debug messages. Overrides log_level.",
    )
    parser.add_argument(
        '-u', '--user', action='store', help="The owner of the process."
    )
    parsed_args = parser.parse_args()

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
    if parsed_args.user:
        result['user'] = parsed_args.user

    return result


def _get_reinterpreted_raw_values(config):
    result: dict[str, Any] = {'websocket': {}}

    ssl_context = None
    if config['websocket']['certificate'] and config['websocket']['private_key']:
        logger.warning(
            'Using service SSL configuration is deprecated. Please use NGINX instead.'
        )
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.load_cert_chain(
            config['websocket']['certificate'], config['websocket']['private_key']
        )
    result['websocket']['ssl'] = ssl_context

    result['log_level'] = get_log_level_by_name(config['log_level'])

    return result


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
