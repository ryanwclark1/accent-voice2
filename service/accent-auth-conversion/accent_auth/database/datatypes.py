# Copyright 2023 Accent Communications

import sqlalchemy.types as types


class XMLPostgresqlType(types.UserDefinedType):
    cache_ok = True

    def get_col_spec(self, **kw):
        return "XML"

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process
