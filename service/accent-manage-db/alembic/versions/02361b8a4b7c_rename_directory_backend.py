"""rename-directory-backend

Revision ID: 02361b8a4b7c
Revises: 30271471ab8

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '02361b8a4b7c'
down_revision = '30271471ab8'

directories_table = sa.sql.table(
    'directories',
    sa.sql.column('dirtype'),
)


def _update_type(from_, to):
    op.execute(
        directories_table
        .update()
        .where(directories_table.c.dirtype == from_)
        .values(dirtype=to)
    )


def upgrade():
    _update_type(from_='accent', to='accent')


def downgrade():
    _update_type(from_='accent', to='accent')
