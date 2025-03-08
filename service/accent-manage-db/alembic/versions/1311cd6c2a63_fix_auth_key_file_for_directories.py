"""fix-auth-key-file-for-directories

Revision ID: 1311cd6c2a63
Revises: 71c41130380e

"""

import sqlalchemy as sa
from sqlalchemy import sql

from alembic import op

# revision identifiers, used by Alembic.
revision = '1311cd6c2a63'
down_revision = '71c41130380e'

directories = sa.sql.table(
    'directories',
    sa.sql.column('dirtype'),
    sa.sql.column('accent_username'),
    sa.sql.column('accent_password'),
    sa.sql.column('auth_key_file'),
)


def _set_default_auth_key_file():
    query = (
        directories.update()
        .where(
            sql.and_(
                directories.c.dirtype == 'accent',
                directories.c.accent_username == 'accent-dird-accent-backend',
            )
        )
        .values(
            auth_key_file='/var/lib/accent-auth-keys/accent-dird-accent-backend-key.yml',
            accent_password=None,
        )
    )
    op.execute(query)


def upgrade():
    _set_default_auth_key_file()


def downgrade():
    pass
