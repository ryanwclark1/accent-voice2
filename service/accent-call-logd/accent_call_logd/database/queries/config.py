# Copyright 2023 Accent Communications

from ..models import Config
from .base import BaseDAO

DEFAULT_CDR_DAYS = 365
DEFAULT_EXPORT_DAYS = 2
DEFAULT_RECORDING_DAYS = 365


class ConfigDAO(BaseDAO):
    def find_or_create(self):
        with self.new_session() as session:
            config = session.query(Config).first()
            if not config:
                config = Config(
                    retention_cdr_days=DEFAULT_CDR_DAYS,
                    retention_cdr_days_from_file=False,
                    retention_export_days=DEFAULT_EXPORT_DAYS,
                    retention_export_days_from_file=False,
                    retention_recording_days=DEFAULT_RECORDING_DAYS,
                    retention_recording_days_from_file=False,
                )
                session.add(config)
            session.flush()
            session.expunge(config)
        return config

    def update(self, config):
        with self.new_session() as session:
            session.add(config)
            session.flush()
            session.expunge(config)
