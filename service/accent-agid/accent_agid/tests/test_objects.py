# Copyright 2023 Accent Communications

from __future__ import annotations

from unittest import TestCase

from hamcrest import assert_that, is_

from ..objects import VMBox


class VMBoxFastInit(VMBox):
    def __init__(self):
        pass


class TestVMBox(TestCase):
    def test_voicemail_has_password_with_no_password(self):
        vmbox = VMBoxFastInit()
        vmbox.password = ''
        vmbox.skipcheckpass = 0

        assert_that(vmbox.has_password(), is_(False))

    def test_voicemail_has_password_with_password(self):
        vmbox = VMBoxFastInit()
        vmbox.password = '1234'
        vmbox.skipcheckpass = 0

        assert_that(vmbox.has_password(), is_(True))

    def test_voicemail_has_password_no_skip_pass(self):
        vmbox = VMBoxFastInit()
        vmbox.password = '1234'
        vmbox.skipcheckpass = 0

        assert_that(vmbox.has_password(), is_(True))

    def test_voicemail_has_password_skip_pass(self):
        vmbox = VMBoxFastInit()
        vmbox.password = '1234'
        vmbox.skipcheckpass = 1

        assert_that(vmbox.has_password(), is_(False))
