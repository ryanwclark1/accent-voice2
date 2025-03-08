# Copyright 2023 Accent Communications

import os
import shutil
import tempfile
import unittest
from unittest.mock import Mock

from visualplan.html import HTMLVisualizer


class TestHTMLVisualizer(unittest.TestCase):
    def setUp(self):
        self._analyses = [self._new_analysis()]
        self._create_temp_directory()

    def _new_analysis(self):
        analysis = Mock()
        analysis.line_analyses = []
        return analysis

    def tearDown(self):
        self._remove_temp_directory()

    def _create_temp_directory(self):
        self._tmp_dir = tempfile.mkdtemp()

    def _remove_temp_directory(self):
        shutil.rmtree(self._tmp_dir)

    def _list_temp_directory(self):
        return os.listdir(self._tmp_dir)

    def test_write_html_create_the_right_file(self):
        visualizer = self._new_visualizer('test.html')

        visualizer.write(self._analyses)

        self.assertEqual(['test.html'], self._list_temp_directory())

    def _new_visualizer(self, filename):
        abs_filename = os.path.join(self._tmp_dir, filename)
        return HTMLVisualizer(abs_filename)
