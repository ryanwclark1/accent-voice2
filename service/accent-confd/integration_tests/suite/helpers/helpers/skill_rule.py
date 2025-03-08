# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_skill_rule(**parameters):
    parameters.setdefault('name', generate_name())
    return add_skill_rule(**parameters)


def add_skill_rule(accent_tenant=None, **parameters):
    response = confd.queues.skillrules.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_skill_rule(skill_rule_id, check=False, **parameters):
    response = confd.queues.skillrules(skill_rule_id).delete()
    if check:
        response.assert_ok()


def generate_name():
    response = confd.queues.skillrules.get()
    names = set(d['name'] for d in response.items)
    return _random_name(names)


def _random_name(names):
    name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    if name in names:
        return _random_name(names)
    return name
