# Copyright 2023 Accent Communications

from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Any

from accent_provd_client import Client as ProvdClient
from accent_test_helpers import until

from .operation import operation_successful

if TYPE_CHECKING:
    from accent_provd.devices.schemas import BaseDeviceDict, ConfigDict

PLUGIN_TO_INSTALL = 'test-plugin'
LEGACY_PLUGIN_TO_INSTALL = 'test-plugin-legacy-import'


class Device:
    device_counter = 0

    def __init__(
        self,
        client: ProvdClient,
        delete_on_exit: bool = True,
        tenant_uuid: str | None = None,
    ) -> None:
        self._client = client
        self._device: BaseDeviceDict = None  # type: ignore[assignment]
        self._delete_on_exit = delete_on_exit
        self._tenant_uuid = tenant_uuid

    def __enter__(self) -> BaseDeviceDict:
        Device.device_counter += 1
        config: BaseDeviceDict = {
            'config': 'defaultconfigdevice',
            'configured': True,
            'description': 'Test device',
            'id': f'testdevice{Device.device_counter}',
            'ip': '10.0.0.2',
            'mac': '00:11:22:33:44:55',
            'model': 'testdevice',
            'plugin': PLUGIN_TO_INSTALL,
            'vendor': 'test',
            'version': '1.0',
        }
        device = self._client.devices.create(config, tenant_uuid=self._tenant_uuid)
        self._device = self._client.devices.get(
            device['id'], tenant_uuid=self._tenant_uuid
        )
        return self._device

    def __exit__(
        self,
        exec_type: type[BaseException] | None,
        exception: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        if self._delete_on_exit:
            Device.device_counter -= 1
            self._client.devices.delete(self._device['id'])


class Plugin:
    def __init__(self, client: ProvdClient, delete_on_exit: bool = True) -> None:
        self._client = client
        self._plugin = None
        self._delete_on_exit = delete_on_exit

    def __enter__(self) -> dict[str, Any] | None:
        with self._client.plugins.update() as current_operation:
            until.assert_(
                operation_successful, current_operation, tries=20, interval=0.5
            )

        with self._client.plugins.install(PLUGIN_TO_INSTALL) as current_operation:
            until.assert_(
                operation_successful, current_operation, tries=20, interval=0.5
            )

        self._plugin = self._client.plugins.get(PLUGIN_TO_INSTALL)
        return self._plugin

    def __exit__(
        self,
        exec_type: type[BaseException] | None,
        exception: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        if self._delete_on_exit:
            self._client.plugins.uninstall(PLUGIN_TO_INSTALL)


class Configuration:
    def __init__(self, client: ProvdClient, delete_on_exit: bool = True) -> None:
        self._client = client
        self._config: ConfigDict = None  # type: ignore[assignment]
        self._delete_on_exit = delete_on_exit

    def __enter__(self) -> ConfigDict:
        config = {
            'id': 'test1',
            'parent_ids': ['base'],
            'deletable': True,
            'X_type': 'internal',
            'raw_config': {
                'ip': '127.0.0.1',
                'http_port': 8667,
                'ntp_ip': '127.0.0.1',
                'X_accent_phonebook_ip': '127.0.0.1',
                'ntp_enabled': True,
            },
        }
        result = self._client.configs.create(config)
        self._config = self._client.configs.get(result['id'])
        return self._config

    def __exit__(
        self,
        exec_type: type[BaseException] | None,
        exception: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        if self._delete_on_exit:
            self._client.configs.delete(self._config['id'])
