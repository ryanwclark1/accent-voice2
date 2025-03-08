# Copyright 2023 Accent Communications

import json
import os
import unittest
from xml.etree import ElementTree

from ..main import extract_pjsip_doc

TEST_DIR = os.path.dirname(__file__)
INPUT_PATH = os.path.join(TEST_DIR, "core-en_US.xml")
EXPECTED_RESULT_PATH = os.path.join(TEST_DIR, "extracted.json")

XML_ROOT = ElementTree.parse(INPUT_PATH).getroot()


class TestPJSIPDocExtractor(unittest.TestCase):
    def test_conversion(self):
        result = extract_pjsip_doc(XML_ROOT)

        with open(EXPECTED_RESULT_PATH) as f:
            expected = json.load(f)

        assert result == expected
