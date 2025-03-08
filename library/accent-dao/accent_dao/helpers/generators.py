# Copyright 2023 Accent Communications

import random
import string

ALPHANUMERIC_POOL = string.ascii_lowercase + string.digits


def find_unused_hash(already_exists_predicate):
    while True:
        data = generate_hash()
        if not already_exists_predicate(data):
            return data


def generate_hash(length=8):
    return ''.join(random.choice(ALPHANUMERIC_POOL) for _ in range(length))
