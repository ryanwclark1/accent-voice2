# Copyright 2023 Accent Communications

import random
import re
import string


class Slug:
    _ALLOWED_CHARS = 'a-zA-Z0-9_-'
    _MAX_LENGTH = 80

    @classmethod
    def from_name(cls, name):
        return re.sub(f'[^{cls._ALLOWED_CHARS}]', '', name)[: cls._MAX_LENGTH]

    @classmethod
    def valid_re(cls):
        return f'^[{cls._ALLOWED_CHARS}]+$'

    @classmethod
    def random(cls, length):
        assert length < cls._MAX_LENGTH

        choices = string.ascii_lowercase + string.digits
        return ''.join(random.choice(choices) for _ in range(length))


class TenantSlug(Slug):
    _ALLOWED_CHARS = 'a-zA-Z0-9_'
    _MAX_LENGTH = 10
