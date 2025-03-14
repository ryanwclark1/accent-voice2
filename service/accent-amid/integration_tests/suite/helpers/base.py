# Copyright 2023 Accent Communications

import logging
import os
import random
import string
import unittest
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

import requests
import yaml
from accent_amid_client import Client as AmidClient
from accent_test_helpers.asset_launching_test_case import (
    AssetLaunchingTestCase,
    NoSuchPort,
    NoSuchService,
    WrongClient,
)
from accent_test_helpers.bus import BusClient
from accent_test_helpers.filesystem import FileSystemClient
from hamcrest import assert_that, equal_to

from .wait_strategy import EverythingOkWaitStrategy

logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()  # type: ignore

ASSETS_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')

VALID_TOKEN = 'valid-token-multitenant'
TOKEN_SUB_TENANT = 'valid-token-sub-tenant'
SERVICE_RABBITMQ = 'rabbitmq'
SERVICE_ASTERISK_AMI = 'asterisk-ami'
SERVICE_ASTERISK_AJAM = 'asterisk-ajam'
SERVICE_AUTH = 'auth'
SERVICE_AMID = 'amid'


class APIAssetLaunchingTestCase(AssetLaunchingTestCase):
    assets_root = ASSETS_ROOT
    asset = 'base'
    service = SERVICE_AMID
    wait_strategy = EverythingOkWaitStrategy()

    @classmethod
    def make_amid(cls, token: str = VALID_TOKEN) -> AmidClient:
        try:
            port = cls.service_port(9491, SERVICE_AMID)
        except NoSuchService:
            return WrongClient(SERVICE_AMID)
        return AmidClient(
            '127.0.0.1',
            port=port,
            prefix=None,
            https=False,
            token=token,
        )

    @classmethod
    def make_bus(cls) -> BusClient:
        try:
            port = cls.service_port(5672, SERVICE_RABBITMQ)
        except NoSuchService:
            return WrongClient(SERVICE_RABBITMQ)
        bus = BusClient.from_connection_fields(
            host='127.0.0.1',
            port=port,
            exchange_name='accent-headers',
            exchange_type='headers',
        )
        return bus

    @classmethod
    def make_ajam_base_url(cls) -> str:
        try:
            ajam_port = cls.service_port(5039, SERVICE_ASTERISK_AJAM)
        except (NoSuchPort, NoSuchService):
            ajam_port = None
        return f'http://127.0.0.1:{ajam_port}'

    @classmethod
    def make_send_event_ami_url(cls) -> str:
        try:
            send_event_ami_port = cls.service_port(8123, SERVICE_ASTERISK_AMI)
        except (NoSuchPort, NoSuchService):
            send_event_ami_port = None
        return f'http://127.0.0.1:{send_event_ami_port}/send_event'


class APIIntegrationTest(unittest.TestCase):
    amid: AmidClient
    ajam_base_url: str
    asset_cls = APIAssetLaunchingTestCase

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.reset_clients()
        cls.asset_cls.wait_strategy.wait(cls)

    def setUp(self) -> None:
        super().setUp()
        self.amid.set_token(VALID_TOKEN)

    @classmethod
    def reset_clients(cls) -> None:
        cls.amid = cls.asset_cls.make_amid()
        cls.ajam_base_url = cls.asset_cls.make_ajam_base_url()

    @classmethod
    def ajam_url(cls, *parts: str) -> str:
        path = '/'.join(parts)
        return f'{cls.ajam_base_url}/{path}'

    @classmethod
    def restart_amid(cls) -> None:
        cls.asset_cls.restart_service('amid')
        cls.amid = cls.asset_cls.make_amid()

    @classmethod
    @contextmanager
    def amid_with_config_file(cls, config: dict) -> Generator[None, None, None]:
        filesystem = FileSystemClient(
            execute=cls.asset_cls.docker_exec,
            service_name='amid',
            root=True,
        )
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        config_file = f'/etc/accent-amid/conf.d/10-{name}.yml'
        content = yaml.dump(config)
        try:
            with filesystem.file_(config_file, content=content):
                cls.restart_amid()
                yield
        finally:
            cls.restart_amid()
            cls.asset_cls.wait_strategy.wait(cls)

    @classmethod
    @contextmanager
    def auth_stopped(cls) -> Generator[None, None, None]:
        cls.asset_cls.stop_service(SERVICE_AUTH)
        try:
            yield
        finally:
            cls.asset_cls.start_service(SERVICE_AUTH)
            cls.reset_clients()

    @classmethod
    @contextmanager
    def ajam_stopped(cls) -> Generator[None, None, None]:
        cls.asset_cls.stop_service(SERVICE_ASTERISK_AJAM)
        try:
            yield
        finally:
            cls.asset_cls.start_service(SERVICE_ASTERISK_AJAM)
            cls.reset_clients()

    @classmethod
    @contextmanager
    def ami_stopped(cls) -> Generator[None, None, None]:
        cls.asset_cls.stop_service(SERVICE_ASTERISK_AMI)
        try:
            yield
        finally:
            cls.asset_cls.start_service(SERVICE_ASTERISK_AMI)

    @classmethod
    @contextmanager
    def rabbitmq_stopped(cls) -> Generator[None, None, None]:
        cls.asset_cls.stop_service(SERVICE_RABBITMQ)
        try:
            yield
        finally:
            cls.asset_cls.start_service(SERVICE_RABBITMQ)

    @classmethod
    def ajam_requests(cls) -> dict[str, Any]:
        response = requests.get(cls.ajam_url('_requests'))
        assert_that(response.status_code, equal_to(200))
        return response.json()
