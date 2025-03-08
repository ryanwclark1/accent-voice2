# Copyright 2023 Accent Communications

from werkzeug.routing import BaseConverter, ValidationError


class FilenameConverter(BaseConverter):
    def to_python(self, value):
        if not value or len(value) > 194:
            raise ValidationError()
        if '/' in value or value.startswith('.'):
            raise ValidationError()
        return value
