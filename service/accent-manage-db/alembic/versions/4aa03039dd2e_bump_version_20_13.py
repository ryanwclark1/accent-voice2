"""bump_version_20_13

Revision ID: 4aa03039dd2e
Revises: d56d7434e9f4

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4aa03039dd2e'
down_revision = 'd56d7434e9f4'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.13'))


def downgrade():
    pass
