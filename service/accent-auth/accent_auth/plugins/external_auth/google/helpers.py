# Copyright 2023 Accent Communications

import time
from datetime import datetime, timedelta


def get_timestamp_expiration(expires_in):
    token_expiration_date = datetime.now() + timedelta(seconds=expires_in)
    return time.mktime(token_expiration_date.timetuple())
