# Copyright 2023 Accent Communications

from accent_dao.alchemy.asterisk_file import AsteriskFile


class AsteriskFilePersistor:
    def __init__(self, session):
        self.session = session

    def find_by(self, **kwargs):
        query = self.session.query(AsteriskFile).filter_by(**kwargs)
        return query.first()

    def edit(self, asterisk_file):
        self.session.add(asterisk_file)
        self.session.flush()

    def edit_section_variables(self, section, variables):
        section.variables = variables
        self.session.flush()
