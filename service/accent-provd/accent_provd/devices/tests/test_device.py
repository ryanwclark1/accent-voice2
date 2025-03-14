# Copyright 2023 Accent Communications

from __future__ import annotations

import unittest

from hamcrest import assert_that, equal_to

from accent_provd.devices.device import copy, needs_reconfiguration
from accent_provd.devices.schemas import DeviceDict


class TestDevice(unittest.TestCase):
    def test_copy_is_a_copy(self) -> None:
        device_orig: DeviceDict = {'id': '1', 'mac': '00:11:22:33:44:55'}

        device_copy = copy(device_orig)

        assert_that(device_copy, equal_to(device_orig))

    def test_copy_has_no_reference_to_orig(self) -> None:
        device_orig = {'id': '1', 'foo': [1]}

        device_copy = copy(device_orig)
        device_copy['foo'].append(2)  # type: ignore

        assert_that(device_orig, equal_to({'id': '1', 'foo': [1]}))

    def test_is_reconfigured_needed_same_device(self) -> None:
        device: DeviceDict = {'id': '1', 'config': 'a', 'tenant_uuid': 'tenant_uuid'}

        self.assertFalse(needs_reconfiguration(device, device))

    def test_is_reconfigured_needed_different_significant_key(self) -> None:
        old_device: DeviceDict = {
            'id': '1',
            'config': 'a',
            'tenant_uuid': 'tenant_uuid',
        }
        new_device: DeviceDict = {
            'id': '1',
            'config': 'b',
            'tenant_uuid': 'tenant_uuid',
        }

        self.assertTrue(needs_reconfiguration(old_device, new_device))

    def test_is_reconfigured_needed_different_insignificant_key(self) -> None:
        old_device: DeviceDict = {
            'id': '1',
            'foo': 'a',  # type: ignore[typeddict-unknown-key]
            'tenant_uuid': 'tenant_uuid',
        }
        new_device: DeviceDict = {
            'id': '1',
            'foo': 'b',  # type: ignore[typeddict-unknown-key]
            'tenant_uuid': 'tenant_uuid',
        }

        self.assertFalse(needs_reconfiguration(old_device, new_device))
