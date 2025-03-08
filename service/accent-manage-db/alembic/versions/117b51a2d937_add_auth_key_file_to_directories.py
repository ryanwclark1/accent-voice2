"""add_auth_key_file_to_directories

Revision ID: 117b51a2d937
Revises: 46dda7d0374e

"""

import sqlalchemy as sa
from sqlalchemy import sql

from alembic import op

# revision identifiers, used by Alembic.
revision = '117b51a2d937'
down_revision = '46dda7d0374e'

TABLE = 'directories'
COLUMN = 'auth_key_file'


def _set_default_auth_key_file():
    directories = sa.sql.table(
        TABLE,
        sa.sql.column('dirtype'),
        sa.sql.column('accent_username'),
        sa.sql.column('accent_password'),
        sa.sql.column('auth_host'),
        sa.sql.column('auth_key_file'),
    )

    query = (
        directories.update()
        .where(
            sql.and_(
                directories.c.dirtype == 'accent',
                directories.c.accent_username == 'accent-dird-accent-backend',
                directories.c.auth_host == 'localhost',
            )
        )
        .values(
            auth_key_file='/var/lib/accent-auth-keys/accent-dird-accent-backend-key.yml',
            accent_password=None,
        )
    )
    op.execute(query)


def upgrade():
    op.add_column(TABLE, sa.Column(COLUMN, sa.Text))
    _set_default_auth_key_file()


def downgrade():
    op.drop_column(TABLE, COLUMN)
