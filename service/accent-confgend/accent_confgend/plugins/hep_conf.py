# Copyright 2023 Accent Communications


from io import StringIO

from accent_dao.resources.asterisk_file import dao as asterisk_file_dao

from ..helpers.asterisk import AsteriskFileGenerator


class HEPConfGenerator:
    def __init__(self, dependencies):
        self.dependencies = dependencies

    def generate(self):
        asterisk_file_generator = AsteriskFileGenerator(asterisk_file_dao)
        output = StringIO()
        asterisk_file_generator.generate('hep.conf', output)
        return output.getvalue()
