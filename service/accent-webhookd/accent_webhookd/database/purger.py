# Copyright 2023 Accent Communications

import datetime

from sqlalchemy import func

from .models import SubscriptionLog


class SubscriptionLogsPurger:
    def purge(self, days_to_keep, session):
        query = SubscriptionLog.__table__.delete().where(
            SubscriptionLog.started_at
            < (func.localtimestamp() - datetime.timedelta(days=days_to_keep))
        )
        session.execute(query)
