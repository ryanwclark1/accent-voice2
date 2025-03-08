# Copyright 2023 Accent Communications

from accent_dao.alchemy.iaxcallnumberlimits import IAXCallNumberLimits


class IAXCallNumberLimitsPersistor:
    def __init__(self, session):
        self.session = session

    def find_all(self):
        query = self.session.query(IAXCallNumberLimits)
        return query.all()

    def edit_all(self, iax_callnumberlimits):
        self.session.query(IAXCallNumberLimits).delete()
        self.session.add_all(iax_callnumberlimits)
        self.session.flush()
