# Copyright 2023 Accent Communications

from __future__ import annotations

import os
import sys

from accent_uuid.uuid_ import get_accent_uuid

from accent_manage_db import alembic
from accent_manage_db.exception import DBError


def main() -> None:
    os.environ["ACCENT_UUID"] = get_accent_uuid()

    print("Updating database...")
    try:
        alembic.update_db()
        print("Updating database done.")
    except DBError:
        sys.exit(1)
