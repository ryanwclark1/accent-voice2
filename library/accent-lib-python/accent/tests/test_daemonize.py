# Copyright 2023 Accent Communications

import unittest
from unittest.mock import patch, sentinel

from accent import daemonize


@patch("accent.daemonize.unlock_pidfile")
@patch("accent.daemonize.lock_pidfile_or_die")
class TestPidfileContext(unittest.TestCase):
    def test_that_lock_is_called(self, lock_fn, _unlock_fn):
        with daemonize.pidfile_context(sentinel.filename):
            lock_fn.assert_called_once_with(sentinel.filename)

    def test_that_unlock_is_called(self, _lock_fn, unlock_fn):
        with daemonize.pidfile_context(sentinel.filename):
            pass

        unlock_fn.assert_called_once_with(sentinel.filename)

    def test_that_unlock_is_called_on_exception(self, _lock_fn, unlock_fn):
        def f():
            with daemonize.pidfile_context(sentinel.filename):
                raise Exception("ok")

        self.assertRaises(Exception, f)

        unlock_fn.assert_called_once_with(sentinel.filename)
