# Copyright 2023 Accent Communications
from textwrap import dedent
from unittest.mock import call, mock_open

import pytest

from . import load_from_sbin

CONFIG_FILE_PATH = '/etc/odbcinst.ini'


@pytest.fixture
def update_odbcinst_config():
    yield load_from_sbin('accent-update-odbcinst-config')


def test_unmodified(update_odbcinst_config):
    config = """
        [accent]
        Description         = Connection to the database used by ACCENT
    """
    update_odbcinst_config.open = mock_open(read_data=dedent(config))
    update_odbcinst_config.main()
    update_odbcinst_config.open.assert_called_once_with(CONFIG_FILE_PATH)


def test_modified_comm_log(update_odbcinst_config):
    config = """
        [PostgreSQL ANSI]
        CommLog = 1
    """
    update_odbcinst_config.open = mock_open(read_data=dedent(config))
    update_odbcinst_config.main()
    update_odbcinst_config.open.assert_has_calls(
        [
            call(CONFIG_FILE_PATH),
            call().__enter__(),
            call().__getattr__('__iter__')(),
            call().__exit__(None, None, None),
            call(CONFIG_FILE_PATH, 'w'),
            call().__enter__(),
            call().write('[PostgreSQL ANSI]\n'),
            call().write('CommLog = 0\n'),
            call().write('\n'),
            call().__exit__(None, None, None),
        ]
    )


def test_removes_pooling_and_odbc(update_odbcinst_config):
    config = """
        [accent]

        [ODBC]
        Pooling = 1
    """
    update_odbcinst_config.open = mock_open(read_data=dedent(config))
    update_odbcinst_config.main()
    update_odbcinst_config.open.assert_has_calls(
        [
            call(CONFIG_FILE_PATH),
            call().__enter__(),
            call().__getattr__('__iter__')(),
            call().__exit__(None, None, None),
            call(CONFIG_FILE_PATH, 'w'),
            call().__enter__(),
            call().write('[accent]\n'),
            call().write('\n'),
            call().__exit__(None, None, None),
        ]
    )
