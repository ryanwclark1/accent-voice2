# Copyright 2023 Accent Communications

import logging

from accent.chain_map import ChainMap
from accent.config_helper import parse_config_dir, read_config_file_hierarchy

logger = logging.getLogger(__name__)

_APP_NAME = 'accent-auth-cli'
_DEFAULT_CONFIG = {
    'config_file': f'/etc/{_APP_NAME}/config.yml',
    'extra_config_files': f'/etc/{_APP_NAME}/conf.d/',
    'auth': {'host': 'localhost', 'port': 9497, 'prefix': None, 'https': False},
}

_AUTH_ARGS_TO_FIELDS_MAP = {
    'auth_username': 'username',
    'hostname': 'host',
    'auth_password': 'password',
    'port': 'port',
    'backend': 'backend',
}


def _args_to_dict(parsed_args):
    auth_config = {}
    for arg_name, config_name in _AUTH_ARGS_TO_FIELDS_MAP.items():
        value = getattr(parsed_args, arg_name, None)
        if value is None:
            continue
        logger.debug('setting %s = %s', config_name, value)
        auth_config[config_name] = value

    if parsed_args.ssl:
        auth_config['https'] = True
    if parsed_args.no_ssl:
        auth_config['https'] = False
    if parsed_args.verify:
        auth_config['verify_certificate'] = True
    elif parsed_args.insecure:
        auth_config['verify_certificate'] = False
    elif parsed_args.cacert:
        auth_config['verify_certificate'] = parsed_args.cacert

    config = {'auth': auth_config}
    return config


def _read_user_config(parsed_args):
    if not parsed_args.config:
        return {}
    configs = parse_config_dir(parsed_args.config)
    return ChainMap(*configs)


def build(parsed_args):
    cli_config = _args_to_dict(parsed_args)
    user_file_config = _read_user_config(parsed_args)
    system_file_config = read_config_file_hierarchy(
        ChainMap(cli_config, user_file_config, _DEFAULT_CONFIG)
    )
    final_config = ChainMap(
        cli_config, user_file_config, system_file_config, _DEFAULT_CONFIG
    )
    return final_config
