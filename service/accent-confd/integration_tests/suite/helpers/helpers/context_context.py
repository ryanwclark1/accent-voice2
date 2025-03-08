# Copyright 2023 Accent Communications

from . import confd


def associate(context_id, context_ids, check=True):
    contexts = [{'id': c_id} for c_id in context_ids]
    response = confd.contexts(context_id).contexts.put(contexts=contexts)
    if check:
        response.assert_ok()


def dissociate(context_id, check=True):
    response = confd.contexts(context_id).contexts.put(contexts=[])
    if check:
        response.assert_ok()
