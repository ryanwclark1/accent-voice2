"""bump_version_24_10

Revision ID: 442b09d80585
Revises: de39965fa6f6

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '442b09d80585'
down_revision = 'de39965fa6f6'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.10'))


def downgrade():
    pass
