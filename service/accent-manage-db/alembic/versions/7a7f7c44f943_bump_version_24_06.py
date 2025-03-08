"""bump_version_24_06

Revision ID: 7a7f7c44f943
Revises: bbccbc1248d8

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '7a7f7c44f943'
down_revision = 'bbccbc1248d8'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.06'))


def downgrade():
    pass
