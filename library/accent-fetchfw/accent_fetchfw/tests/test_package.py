# Copyright 2023 Accent Communications

from unittest import TestCase

import accent_fetchfw.package as package


class TestInstalledPackage(TestCase):
    def test_ok_on_all_mandatory_keys_specified(self):
        pkg_info = {'id': 'foo', 'description': 'Foo', 'version': '1', 'files': [], 'explicit_install': True}
        package.InstalledPackage(pkg_info)

    def test_raise_error_on_missing_mandatory_key(self):
        pkg_info = {
            'id': 'foo',
            'description': 'Foo',
            'version': '1',
            'files': [],
        }
        self.assertRaises(Exception, package.InstalledPackage, pkg_info)


class TestInstallablePackage(TestCase):
    def test_ok_on_all_mandatory_keys_specified(self):
        pkg_info = {'id': 'foo', 'description': 'Foo', 'version': '1'}
        package.InstallablePackage(pkg_info, [], None)

    def test_raise_error_on_missing_mandatory_key(self):
        pkg_info = {'id': 'foo', 'description': 'Foo'}
        self.assertRaises(Exception, package.InstallablePackage, pkg_info, [], None)
