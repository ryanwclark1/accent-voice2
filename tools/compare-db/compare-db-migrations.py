import argparse
import io
import logging
import os
import sys
from configparser import ConfigParser

import accent_dao.alchemy.all  # noqa
import sh
import sqlalchemy as sa
import sqlalchemy_utils
from accent_dao.helpers import db_manager
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

LOG_FORMAT = '%(asctime)s [%(process)d] (%(levelname)s) (%(name)s): %(message)s'

logging.getLogger('sh.stream_bufferer').setLevel(logging.WARNING)
logging.getLogger('sh.streamreader').setLevel(logging.WARNING)
logging.getLogger('sh.command').setLevel(logging.WARNING)
logging.getLogger('alembic.runtime.migration').setLevel(logging.WARNING)

logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger('compare-db-migrations')

CWD_PATH = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser()
config.read(os.path.join(CWD_PATH, 'defaults.ini'))

os.environ.pop('ALEMBIC_DB_URI', None)


def argparser():
    parser = argparse.ArgumentParser('Compare Accent database schemas and check for inconsistencies')
    parser.add_argument('--config', help='config file')
    return parser


def main():
    parser = argparser()
    args = parser.parse_args()

    if args.config:
        config.read(args.config)

    installed_postgresql_uri = config.get('database_uri', 'installed')
    migrated_postgresql_uri = config.get('database_uri', 'migrated')

    logger.info('Generating freshly installed database...')
    generate_installed_database(installed_postgresql_uri)
    logger.info('Generating migrated database...')
    generate_migrated_database(migrated_postgresql_uri)

    differences = compare_schemas(migrated_postgresql_uri, installed_postgresql_uri)

    if differences:
        logger.error("Differences detected from migrated to installed schema.")
        logger.error(
            "These commands show what migration script should be added"
            "in order to obtain the same schema as a fresh install.\n"
            + str(differences)
        )
        sys.exit(1)


def generate_installed_database(postgresql_uri):
    alembic_cfg = build_alembic_config(postgresql_uri)

    reset_database(postgresql_uri)
    create_tables(postgresql_uri)
    populate_db(postgresql_uri)
    # make sure stamp doesn't show up in diff
    alembic_command.stamp(alembic_cfg, 'head')


def generate_migrated_database(postgresql_uri):
    script = os.path.join(CWD_PATH, 'asterisk_migration.sql')

    reset_database(postgresql_uri)
    run_script(script, postgresql_uri)
    run_alembic_migrations(postgresql_uri)


def reset_database(postgresql_uri):
    drop_database(postgresql_uri)
    create_database(postgresql_uri)
    enable_extensions(postgresql_uri)


def drop_database(postgresql_uri):
    logger.info("dropping database")
    if sqlalchemy_utils.functions.database_exists(postgresql_uri):
        engine = sa.create_engine(postgresql_uri)
        engine.execute('DROP OWNED BY asterisk CASCADE;')
        engine.execute('DROP ROLE IF EXISTS asterisk;')
        engine.dispose()

        sqlalchemy_utils.functions.drop_database(postgresql_uri)


def create_database(postgresql_uri):
    logger.info("creating database")

    sqlalchemy_utils.functions.create_database(postgresql_uri)

    engine = sa.create_engine(postgresql_uri)
    engine.execute('CREATE ROLE asterisk WITH PASSWORD \'superpass\';')
    engine.dispose()


def enable_extensions(postgresql_uri):
    logger.info("enabling DB extensions")
    engine = sa.create_engine(postgresql_uri)
    engine.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    engine.dispose()


def create_tables(postgresql_uri):
    logger.info("creating tables")

    engine = sa.create_engine(postgresql_uri)
    db_manager.Base.metadata.create_all(bind=engine)
    engine.dispose()


def populate_db(postgresql_uri):
    path = "{}/populate/populate.sql".format(config.get('repos', 'manage_db'))
    run_script(path, postgresql_uri)


def run_alembic_migrations(postgresql_uri):
    logger.info("running alembic migrations")
    alembic_cfg = build_alembic_config(postgresql_uri)
    os.environ['ACCENT_UUID'] = '99999999-9999-9999-9999-999999999999'
    alembic_command.stamp(alembic_cfg, 'base')
    alembic_command.upgrade(alembic_cfg, 'head')
    manually_migrate_call_logd_db(postgresql_uri)


# TODO: buster-bullseye migration: ensure those tables are dropped by alembic
# then remove this function
def manually_migrate_call_logd_db(postgresql_uri):
    run_psql_cmd(postgresql_uri, 'DROP TABLE call_log, call_log_participant;')
    run_psql_cmd(postgresql_uri, 'DROP TYPE call_log_participant_role;')


def run_psql_cmd(postgresql_uri, command):
    error_buffer = io.StringIO()
    sh.psql(
        '-qX',
        d=postgresql_uri,
        c=command,
        _err=error_buffer,
        _env={'PGOPTIONS': '--client-min-messages=warning'},  # prevents NOTICE:
    )
    errors = error_buffer.getvalue()
    if errors:
        logger.warning("errors while executing %s: %s", command, errors)
        sys.exit(2)


def build_alembic_config(postgresql_uri):
    alembic_path = "{}/alembic".format(config.get('repos', 'manage_db'))
    ini_file = "{}/alembic.ini".format(config.get('repos', 'manage_db'))

    alembic_cfg = AlembicConfig(ini_file)
    alembic_cfg.set_main_option('configure_logging', 'false')
    alembic_cfg.set_main_option("script_location", alembic_path)
    alembic_cfg.set_main_option("sqlalchemy.url", postgresql_uri)
    return alembic_cfg


def run_script(filepath, postgresql_uri):
    logger.info("running script %s", filepath)

    error_buffer = io.StringIO()

    sh.psql(
        '-qX',
        d=postgresql_uri,
        f=filepath,
        _err=error_buffer,
        _env={'PGOPTIONS': '--client-min-messages=warning'},  # prevents NOTICE:
    )

    errors = error_buffer.getvalue()
    if errors:
        logger.warning("errors while executing %s: %s", filepath, errors)
        sys.exit(2)


def compare_schemas(migrated_postgresql_uri, installed_postgresql_uri):
    # Return code 0 = no differences found
    # Return code 2 = found differences
    output = sh.migra(
        '--unsafe',
        migrated_postgresql_uri,
        installed_postgresql_uri,
        _ok_code=[0, 2],
    )
    return output


if __name__ == "__main__":
    main()
