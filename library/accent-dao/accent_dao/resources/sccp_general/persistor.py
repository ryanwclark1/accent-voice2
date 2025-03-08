# Copyright 2023 Accent Communications

from accent_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings


class SCCPGeneralPersistor:
    def __init__(self, session):
        self.session = session

    def find_all(self):
        query = self.session.query(SCCPGeneralSettings)
        return query.all()

    def edit_all(self, sccp_general):
        self.session.query(SCCPGeneralSettings).delete()
        self.session.add_all(sccp_general)
        self.session.flush()
