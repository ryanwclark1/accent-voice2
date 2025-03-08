# Copyright 2023 Accent Communications

from accent_dao.alchemy.staticqueue import StaticQueue


class QueueGeneralPersistor:
    def __init__(self, session):
        self.session = session

    def find_all(self):
        query = (
            self.session.query(StaticQueue)
            .filter(StaticQueue.category == 'general')
            .filter(StaticQueue.var_val != None)  # noqa
            .order_by(StaticQueue.var_metric.asc())
        )
        return query.all()

    def edit_all(self, queue_general):
        self.session.query(StaticQueue).filter(
            StaticQueue.category == 'general'
        ).delete()
        self.session.add_all(self._fill_default_values(queue_general))
        self.session.flush()

    def _fill_default_values(self, queue_general):
        for setting in queue_general:
            setting.filename = 'queues.conf'
            setting.category = 'general'
        return queue_general
