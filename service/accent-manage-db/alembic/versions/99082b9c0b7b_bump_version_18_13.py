"""bump_version_18_13

Revision ID: 99082b9c0b7b
Revises: 2256e488e43c

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '99082b9c0b7b'
down_revision = '2256e488e43c'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.13'))


def downgrade():
    pass
