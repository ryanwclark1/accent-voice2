# Copyright 2023 Accent Communications

import logging
import os
import subprocess
import textwrap
from unittest import TestCase

from hamcrest import assert_that, is_

extra_config_path = '/etc/accent-purge-db/conf.d'
extra_config_filename = 'extra-config-sample.yml'
extra_config_file = os.path.join(extra_config_path, extra_config_filename)

archive_output_file = '/tmp/accent_purge_db.archive'
purge_output_file = '/tmp/accent_purge_db.purge'

logger = logging.getLogger(__name__)


class TestSamplePlugin(TestCase):
    def setUp(self):
        extra_config = textwrap.dedent("""
            enabled_plugins:
                purgers:
                     sample: true
                archives:
                    - sample
            db_uri: 'postgresql://asterisk:password123@db/asterisk'
            days_to_keep: 123
            days_to_keep_per_plugin:
                sample: 30
            """)

        with open(extra_config_file, 'w') as config_file:
            config_file.write(extra_config)

    def tearDown(self):
        if os.path.exists(extra_config_file):
            self._run_cmd(f'rm {extra_config_file}')
        if os.path.exists(archive_output_file):
            self._run_cmd(f'rm {archive_output_file}')
        if os.path.exists(purge_output_file):
            self._run_cmd(f'rm {purge_output_file}')

    def _run_cmd(self, cmd):
        process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = process.communicate()
        logger.info(out)

    def test_that_load_plugins_works_with_SamplePlugin(self):
        self._run_cmd('accent-purge-db')

        file_exists = os.path.exists(archive_output_file)

        assert_that(file_exists, is_(True))

        with open(archive_output_file) as f:
            archive_content = f.read()
            assert_that(archive_content, "Save tables before purge. 123 days to keep!")

        file_exists = os.path.exists(purge_output_file)

        assert_that(file_exists, is_(True))

        with open(purge_output_file) as f:
            purge_content = f.read()
            assert_that(purge_content, "Purged, 30 days keeped!")
