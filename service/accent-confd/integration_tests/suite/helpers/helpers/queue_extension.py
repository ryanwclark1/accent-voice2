# Copyright 2023 Accent Communications

from . import db


def associate(queue_id, extension_id, check=True):
    with db.queries() as q:
        q.associate_queue_extension(queue_id, extension_id)


def dissociate(queue_id, extension_id, check=True):
    with db.queries() as q:
        q.dissociate_queue_extension(queue_id, extension_id)
