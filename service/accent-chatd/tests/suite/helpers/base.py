# integration_tests/suite/helpers/base.py

# Copyright 2023 Accent Communications

import logging
import os
import random
import string
import unittest
import uuid
from contextlib import contextmanager

import pytest
import yaml
from accent_chatd_client import Client as ChatdClient
from accent_test_helpers import until
from accent_test_helpers.asset_launching_test_case import (
    AssetLaunchingTestCase,
    NoSuchPort,
    NoSuchService,
)
from accent_test_helpers.auth import AuthClient, MockCredentials, MockUserToken
from accent_test_helpers.filesystem import FileSystemClient

from accent_chatd.database.helpers import Session, init_db
from accent_chatd.database.queries import DAO

# from accent_chatd.core.asyncio_ import get_aio_core # REMOVE
from accent_chatd.core.bus import (
    BusConsumer,
    BusPublisher,
    get_bus_consumer,
    get_bus_publisher,
)  # Import

from .amid import AmidClient

# from .bus import BusClient # REMOVE
from .confd import ConfdClient
from .microsoft import MicrosoftGraphClient
from .wait_strategy import (
    EverythingOkWaitStrategy,
    NoWaitStrategy,
    PresenceInitOkWaitStrategy,
)

DB_URI = "postgresql://accent-chatd:password123@127.0.0.1:{port}"
DB_ECHO = os.getenv("DB_ECHO", "").lower() == "true"

START_TIMEOUT = int(os.environ.get("INTEGRATION_TEST_TIMEOUT", "30"))

TOKEN_UUID = uuid.UUID("00000000-0000-0000-0000-000000000101")
TOKEN_TENANT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000201")
TOKEN_SUBTENANT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000202")
TOKEN_USER_UUID = uuid.UUID("00000000-0000-0000-0000-000000000301")

CHATD_TOKEN_TENANT_UUID = TOKEN_TENANT_UUID

UNKNOWN_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")
ACCENT_UUID = uuid.UUID("00000000-0000-0000-0000-0000000c4a7d")

logger = logging.getLogger(__name__)

use_asset = pytest.mark.usefixtures


class ClientCreateException(Exception):
    def __init__(self, client_name):
        super().__init__(f"Could not create client {client_name}")


class WrongClient:
    def __init__(self, client_name):
        self.client_name = client_name

    def __getattr__(self, member):
        raise ClientCreateException(self.client_name)


class _BaseAssetLaunchingTestCase(AssetLaunchingTestCase):
    assets_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "assets")
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chatd = cls.make_chatd()
        cls.auth = cls.make_auth()
        cls.create_token()
        cls.wait_strategy.wait(cls)

    @classmethod
    def create_token(cls):
        if isinstance(cls.auth, WrongClient):
            return

        token = MockUserToken(
            str(TOKEN_UUID),
            str(TOKEN_USER_UUID),
            metadata={
                "uuid": str(TOKEN_USER_UUID),
                "tenant_uuid": str(TOKEN_TENANT_UUID),
            },
        )
        cls.auth.set_token(token)
        credential = MockCredentials("chatd-service", "chatd-password")
        cls.auth.set_valid_credentials(credential, str(TOKEN_UUID))
        cls.auth.set_tenants(
            {
                "uuid": str(TOKEN_TENANT_UUID),
                "name": "name1",
                "parent_uuid": str(TOKEN_TENANT_UUID),
            },
            {
                "uuid": str(TOKEN_SUBTENANT_UUID),
                "name": "name2",
                "parent_uuid": str(TOKEN_TENANT_UUID),
            },
        )

    @classmethod
    def create_user_token(
        cls, user_uuid=TOKEN_USER_UUID, tenant_uuid=TOKEN_TENANT_UUID
    ):
        if isinstance(cls.auth, WrongClient):
            return

        token = MockUserToken(
            str(uuid.uuid5(uuid.UUID(user_uuid), "token")),
            str(user_uuid),
            metadata={"uuid": str(user_uuid), "tenant_uuid": str(tenant_uuid)},
        )
        cls.auth.set_token(token)
        credential = MockCredentials("username", "password")
        cls.auth.set_valid_credentials(credential, token.token_id)
        return token.token_id

    @classmethod
    def make_db_session(cls):
        try:
            port = cls.service_port(5432, "postgres")
        except (NoSuchService, NoSuchPort):
            return WrongClient("postgres")

        init_db(DB_URI.format(port=port), echo=DB_ECHO)
        return Session

    @classmethod
    def make_chatd(cls, token=str(TOKEN_UUID)):
        try:
            port = cls.service_port(9304, "chatd")
        except (NoSuchService, NoSuchPort):
            return WrongClient("chatd")
        return ChatdClient(
            "127.0.0.1",
            port=port,
            prefix=None,
            https=False,
            token=token,
        )

    @classmethod
    def make_amid(cls):
        try:
            port = cls.service_port(9491, "amid")
        except (NoSuchService, NoSuchPort):
            return WrongClient("amid")
        return AmidClient("127.0.0.1", port=port)

    @classmethod
    def make_auth(cls):
        try:
            port = cls.service_port(9497, "auth")
        except (NoSuchService, NoSuchPort):
            return WrongClient("auth")
        return AuthClient("127.0.0.1", port=port)

    @classmethod
    def make_confd(cls):
        try:
            port = cls.service_port(9486, "confd")
        except NoSuchService:
            return WrongClient("confd")
        return ConfdClient("127.0.0.1", port=port)

    @classmethod
    def make_bus(cls):
        try:
            port = cls.service_port(5672, "rabbitmq")
        except (NoSuchService, NoSuchPort):
            return WrongClient("rabbitmq")
        settings = get_settings()
        return BusPublisher(
            settings.bus.get_connection_url(), settings.bus.exchange_name
        )  # get settings, and connection url.

    @classmethod
    def make_bus_consumer(cls):
        try:
            port = cls.service_port(5672, "rabbitmq")
        except (NoSuchService, NoSuchPort):
            return WrongClient("rabbitmq")
        settings = get_settings()
        return BusConsumer(
            settings.bus.get_connection_url(),
            settings.bus.exchange_name,
            f"test-accent-chatd-{settings.uuid}",
        )  # Create unique name.

    @classmethod
    def start_auth_service(cls):
        cls.start_service("auth")
        cls.auth = cls.make_auth()
        until.true(cls.auth.is_up, tries=5)
        cls.create_token()

    @classmethod
    def stop_auth_service(cls):
        cls.stop_service("auth")

    @classmethod
    def start_chatd_service(cls):
        cls.start_service("chatd")
        cls.chatd = cls.make_chatd()

    @classmethod
    def stop_chatd_service(cls):
        cls.stop_service("chatd")

    @classmethod
    def restart_chatd_service(cls):
        cls.restart_service("chatd")
        cls.chatd = cls.make_chatd()


class APIAssetLaunchingTestCase(_BaseAssetLaunchingTestCase):
    asset = "base"
    service = "chatd"
    wait_strategy = EverythingOkWaitStrategy()


class TeamsAssetLaunchingTestCase(_BaseAssetLaunchingTestCase):
    asset = "teams"
    service = "chatd"
    wait_strategy = EverythingOkWaitStrategy()

    @classmethod
    def make_microsoft(cls):
        try:
            port = cls.service_port(9991, "microsoft")
        except (NoSuchService, NoSuchPort):
            return WrongClient("amid")
        return MicrosoftGraphClient("127.0.0.1", port=port)


class InitAssetLaunchingTestCase(_BaseAssetLaunchingTestCase):
    asset = "initialization"
    service = "chatd"
    wait_strategy = PresenceInitOkWaitStrategy()


class DBAssetLaunchingTestCase(_BaseAssetLaunchingTestCase):
    asset = "database"
    service = "postgres"
    wait_strategy = NoWaitStrategy()


class _BaseIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._Session = cls.asset_cls.make_db_session()

    @classmethod
    def tearDownClass(cls):
        cls._Session.get_bind().dispose()
        cls._Session.remove()

    @property
    def _session(self):
        return self._Session()

    @contextmanager
    def user_token(self, user_uuid):
        token = type(self).asset_cls.create_user_token(user_uuid)
        chatd = self.chatd
        self.chatd = self.asset_cls.make_chatd(token=token)
        yield
        self.__dict__.pop("chatd", None)
        assert self.chatd is chatd

    @classmethod
    def reset_clients(cls):
        cls._Session = cls.asset_cls.make_db_session()
        cls.amid = cls.asset_cls.make_amid()
        cls.chatd = cls.asset_cls.make_chatd()
        cls.auth = cls.asset_cls.make_auth()
        cls.confd = cls.asset_cls.make_confd()
        cls.bus = cls.asset_cls.make_bus()
        cls.bus_consumer = cls.asset_cls.make_bus_consumer()

    @classmethod
    def start_auth_service(cls):
        cls.asset_cls.start_auth_service()
        cls.auth = cls.asset_cls.make_auth()

    @classmethod
    def stop_auth_service(cls):
        cls.asset_cls.stop_auth_service()

    @classmethod
    def start_chatd_service(cls):
        cls.asset_cls.start_chatd_service()
        cls.chatd = cls.asset_cls.make_chatd()

    @classmethod
    def stop_chatd_service(cls):
        cls.asset_cls.stop_chatd_service()

    @classmethod
    def restart_chatd_service(cls):
        cls.asset_cls.restart_chatd_service()
        cls.chatd = cls.asset_cls.make_chatd()

    @classmethod
    def start_amid_service(cls):
        cls.asset_cls.start_service("amid")
        cls.amid = cls.asset_cls.make_amid()

    @classmethod
    def stop_amid_service(cls):
        cls.asset_cls.stop_service("amid")

    @classmethod
    def start_postgres_service(cls):
        cls.asset_cls.start_service("postgres")
        cls._Session = cls.asset_cls.make_db_session()

        def db_is_up():
            try:
                cls._Session.execute("SELECT 1")
            except Exception:
                return False
            return True

        until.true(db_is_up, tries=60)

    @classmethod
    def stop_postgres_service(cls):
        cls._Session.get_bind().dispose()
        cls._Session.remove()
        cls.asset_cls.stop_service("postgres")

    @classmethod
    @contextmanager
    def chatd_with_config(cls, config):
        filesystem = FileSystemClient(
            execute=cls.asset_cls.docker_exec,
            service_name="chatd",
            root=True,
        )
        name = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
        config_file = f"/etc/accent-chatd/conf.d/10-{name}.yml"
        content = yaml.dump(config)
        try:
            with filesystem.file_(config_file, content=content):
                cls.restart_chatd_service()
                yield
        finally:
            cls.restart_chatd_service()
            cls.asset_cls.wait_strategy.wait(cls)

    def setUp(self):
        super().setUp()
        self._dao = DAO()
        self._dao.tenant.find_or_create(TOKEN_TENANT_UUID)
        self._dao.tenant.find_or_create(TOKEN_SUBTENANT_UUID)
        self._session.commit()

    def tearDown(self):
        self._Session.rollback()


class DBIntegrationTest(_BaseIntegrationTest):
    asset_cls = DBAssetLaunchingTestCase


class APIIntegrationTest(_BaseIntegrationTest):
    asset_cls = APIAssetLaunchingTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reset_clients()  # Reset on class setup


class InitIntegrationTest(_BaseIntegrationTest):
    asset_cls = InitAssetLaunchingTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reset_clients()  # Reset on class setup
