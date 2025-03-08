# Copyright 2023 Accent Communications

import unittest

from accent_dao.helpers import errors
from hamcrest import assert_that, calling, equal_to, raises

from ..storage import _SoundFilesystemStorage


class TestBuildPath(unittest.TestCase):
    def test_build_path(self):
        storage = _SoundFilesystemStorage('/tmp')

        result = storage._build_path('one', 'two.three.four', 'five-six_seven')

        assert_that(result, equal_to('/tmp/one/two.three.four/five-six_seven'))

    def test_build_path_dangerous_fragments(self):
        storage = _SoundFilesystemStorage('/tmp')

        assert_that(
            calling(storage._build_path).with_args(
                'one', 'im-a-bad-guy/../../etc/passwd'
            ),
            raises(errors.ResourceError),
        )

    def test_build_path_empty_fragment(self):
        storage = _SoundFilesystemStorage('/tmp')

        result = storage._build_path('one', None, 'two')

        assert_that(result, equal_to('/tmp/one/two'))
