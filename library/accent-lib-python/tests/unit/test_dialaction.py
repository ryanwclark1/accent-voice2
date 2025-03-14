# Copyright 2023 Accent Communications

from unittest import TestCase

from ..dialaction import action, action_subtype, action_type


class TestDialaction(TestCase):
    def test_action(self):
        assert action(None) == ""
        assert action("mytype") == "mytype"
        assert action("mytype", "mysubtype") == "mytype:mysubtype"

    def test_action_type(self):
        assert action_type(None) is None
        assert action_type("mytype") == "mytype"
        assert action_type("mytype:mysubtype") == "mytype"
        assert action_type("mytype:mysubtype:suffix") == "mytype"

    def test_action_subtype(self):
        assert action_subtype(None) is None
        assert action_subtype("mytype") is None
        assert action_subtype("mytype:mysubtype") == "mysubtype"
        assert action_subtype("mytype:mysubtype:suffix") == "mysubtype:suffix"
