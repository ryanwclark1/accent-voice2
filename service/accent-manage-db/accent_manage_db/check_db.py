# Copyright 2023 Accent Communications

from accent_manage_db import alembic


def main() -> None:
    alembic.check_db()
