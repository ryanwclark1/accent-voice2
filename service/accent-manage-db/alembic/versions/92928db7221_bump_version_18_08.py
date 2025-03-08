"""bump_version_18_08

Revision ID: 92928db7221
Revises: c193f30636ff

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '92928db7221'
down_revision = 'c193f30636ff'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.08'))


def downgrade():
    pass
