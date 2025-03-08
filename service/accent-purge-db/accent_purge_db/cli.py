# Copyright 2023 Accent Communications

import argparse
import logging

import accent_dao
from accent.accent_logging import setup_logging
from accent.chain_map import ChainMap
from accent.config_helper import read_config_file_hierarchy
from accent.daemonize import pidfile_context
from accent_dao.helpers.db_utils import session_scope
from stevedore import enabled

_DEFAULT_CONFIG = {
    'pid_file': '/run/accent-purge-db.pid',
    'log_file': '/var/log/accent-purge-db.log',
    'config_file': '/etc/accent-purge-db/config.yml',
    'extra_config_files': '/etc/accent-purge-db/conf.d/',
    'enabled_plugins': {
        'purgers': {
            'cel': True,
            'queue-log': True,
            'stat-agent': True,
            'stat-call-on': True,
            'stat-queue': True,
            'stat-switchboard': True,
        },
        'archives': [],
    },
    'days_to_keep': 365,
    'days_to_keep_per_plugin': {},
}

logger = logging.getLogger(__name__)


def main():
    cli_config = _parse_args()
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    config = ChainMap(cli_config, file_config, _DEFAULT_CONFIG)

    setup_logging(config['log_file'], debug=config['debug'])

    accent_dao.init_db_from_config(config)

    with pidfile_context(config['pid_file']):
        if 'archives' in config.get('enabled_plugins', {}):
            _load_plugins(config)
        _purge_tables(config)


def _load_plugins(config):
    def check_func(extension):
        enabled_archives = config['enabled_plugins']['archives']
        return extension.name in enabled_archives

    enabled.EnabledExtensionManager(
        namespace='accent_purge_db.archives',
        check_func=check_func,
        invoke_args=(config,),
        invoke_on_load=True,
    )


def _purge_tables(config):
    def check_func(extension):
        enabled_purgers = config['enabled_plugins']['purgers']
        return enabled_purgers.get(extension.name, False)

    table_purgers = enabled.EnabledExtensionManager(
        namespace='accent_purge_db.purgers', check_func=check_func, invoke_on_load=True
    )
    with session_scope() as session:
        for purger in table_purgers:
            days_to_keep = config['days_to_keep_per_plugin'].get(purger.name, config['days_to_keep'])
            logger.info(
                '%s purger: deleting entries older than %s days',
                purger.name,
                days_to_keep,
            )
            purger.obj.purge(days_to_keep, session)
            logger.debug('%s purger: finished', purger.name)


def _parse_args():
    config = {}
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--days_to_keep',
        type=int,
        help='Number of days data will be kept in tables',
    )

    parsed_args = parser.parse_args()
    if parsed_args.days_to_keep is not None:
        config['days_to_keep'] = parsed_args.days_to_keep

    return config
