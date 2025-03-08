"""bump_version_21_02

Revision ID: 53ad771ac875
Revises: a10db8de6372

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '53ad771ac875'
down_revision = 'a10db8de6372'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.02'))


def downgrade():
    pass
