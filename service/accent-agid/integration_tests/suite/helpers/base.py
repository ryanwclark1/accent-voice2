# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from pathlib import Path

from accent_test_helpers import until
from accent_test_helpers.asset_launching_test_case import (
    AbstractAssetLaunchingHelper,
    NoSuchPort,
    NoSuchService,
    WrongClient,
    cached_class_property,
)

from .agentd import AgentdMockClient
from .agid import AgidClient
from .calld import CalldMockClient
from .confd import ConfdMockClient
from .database import DbHelper
from .dird import DirdMockClient
from .filesystem import FileSystemClient

DEFAULT_LOG_FORMAT = '%(asctime)s [%(process)d] (%(levelname)s) (%(name)s): %(message)s'
logging.basicConfig(format=DEFAULT_LOG_FORMAT)


class BaseAssetLaunchingHelper(AbstractAssetLaunchingHelper):
    assets_root = Path(__file__).parent / '..' / '..' / 'assets'
    asset = 'base'
    service = 'agid'

    @classmethod
    def reset_clients(cls):
        for attr in ('agid', 'db', 'calld', 'confd', 'agentd', 'filesystem', 'dird'):
            delattr(cls, attr)
        until.true(cls.agid.is_ready, timeout=30)

    @classmethod
    def launch_service_with_asset(cls) -> None:
        """Make sure Agid service is up before starting first test."""
        super().launch_service_with_asset()
        until.true(cls.agid.is_ready, timeout=30)

    @cached_class_property
    def agid(cls) -> AgidClient:
        port = cls.service_port(4573, 'agid')
        return AgidClient('127.0.0.1', port)

    @cached_class_property
    def confd(cls) -> ConfdMockClient:
        port = cls.service_port('9486', 'confd')
        return ConfdMockClient('127.0.0.1', port, version='1.1')

    @cached_class_property
    def agentd(cls) -> AgentdMockClient:
        return AgentdMockClient('127.0.0.1', cls.service_port('9493', 'agentd'))

    @cached_class_property
    def calld(cls) -> CalldMockClient:
        return CalldMockClient('127.0.0.1', cls.service_port('9500', 'calld'))

    @cached_class_property
    def dird(cls) -> DirdMockClient:
        return DirdMockClient(
            '127.0.0.1', cls.service_port('9489', 'dird'), version='0.1'
        )

    @cached_class_property
    def db(cls) -> DbHelper | WrongClient:
        try:
            port = cls.service_port(5432, 'postgres')
        except (NoSuchService, NoSuchPort):
            return WrongClient('postgres')

        # NOTE: Avoid importing accent_agid and dependencies in tests,
        # since no database tests are needed
        return DbHelper.build(
            user='asterisk',
            password='password123',
            host='127.0.0.1',
            port=port,
            db='asterisk',
        )

    @cached_class_property
    def filesystem(cls) -> FileSystemClient:
        return FileSystemClient(execute=cls.docker_exec, service_name=cls.service)
