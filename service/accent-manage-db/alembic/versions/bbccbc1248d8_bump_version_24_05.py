"""bump_version_24_05

Revision ID: bbccbc1248d8
Revises: 40c244ac9a97

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'bbccbc1248d8'
down_revision = '40c244ac9a97'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.05'))


def downgrade():
    pass
