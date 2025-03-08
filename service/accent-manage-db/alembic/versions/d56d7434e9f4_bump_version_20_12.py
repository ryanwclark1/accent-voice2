"""bump_version_20_12

Revision ID: d56d7434e9f4
Revises: 106159225d65

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'd56d7434e9f4'
down_revision = '106159225d65'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.12'))


def downgrade():
    pass
