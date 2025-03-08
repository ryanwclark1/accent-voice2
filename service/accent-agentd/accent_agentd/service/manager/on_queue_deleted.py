# Copyright 2023 Accent Communications

from accent_dao.helpers import db_utils


class OnQueueDeletedManager:
    def __init__(self, agent_status_dao):
        self._agent_status_dao = agent_status_dao

    def on_queue_deleted(self, queue_id):
        with db_utils.session_scope():
            self._agent_status_dao.remove_all_agents_from_queue(queue_id)
