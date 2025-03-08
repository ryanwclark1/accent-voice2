# Copyright 2023 Accent Communications

from . import confd


def associate(queue_id, agent_id, **kwargs):
    check = kwargs.pop('check', True)
    response = confd.queues(queue_id).members.agents(agent_id).put(**kwargs)
    if check:
        response.assert_ok()


def dissociate(queue_id, agent_id, **kwargs):
    check = kwargs.get('check', True)
    response = confd.queues(queue_id).members.agents(agent_id).delete()
    if check:
        response.assert_ok()
