# Copyright 2023 Accent Communications

import logging
import os

import alembic.command
import alembic.config
import alembic.migration
from sqlalchemy import create_engine

from .helpers import wait_is_ready

logger = logging.getLogger(__name__)


def upgrade(uri):
    current_dir = os.path.dirname(__file__)
    config = alembic.config.Config(f'{current_dir}/alembic.ini')
    config.set_main_option('script_location', f'{current_dir}/alembic')
    config.set_main_option('sqlalchemy.url', uri)
    config.set_main_option('configure_logging', 'false')

    logger.info('Upgrading database')
    engine = create_engine(uri)
    wait_is_ready(engine)
    alembic.command.upgrade(config, 'head')
    logger.info('Database upgraded')
