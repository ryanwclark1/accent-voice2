# Copyright 2023 Accent Communications

from hamcrest import assert_that, equal_to, has_properties

from accent_call_logd.database.models import Config

from .helpers.base import DBIntegrationTest


class TestRecording(DBIntegrationTest):
    def test_find_or_create(self):
        result = self.dao.config.find_or_create()
        assert_that(
            result,
            has_properties(
                retention_cdr_days=365,
                retention_export_days=2,
                retention_recording_days=365,
            ),
        )

        self.dao.config.find_or_create()

        result = self.session.query(Config).count()
        assert_that(result, equal_to(1))

        self.session.query(Config).delete()
        self.session.commit()

    def test_update(self):
        config = self.dao.config.find_or_create()
        config.retention_cdr_days = 42
        config.retention_export_days = 10
        config.retention_recording_days = 0
        self.dao.config.update(config)

        result = self.dao.config.find_or_create()
        assert_that(
            result,
            has_properties(
                retention_cdr_days=42,
                retention_export_days=10,
                retention_recording_days=0,
            ),
        )
