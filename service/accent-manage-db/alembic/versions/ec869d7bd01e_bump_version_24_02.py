"""bump_version_24_02

Revision ID: ec869d7bd01e
Revises: e1c0718176ec

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'ec869d7bd01e'
down_revision = 'e1c0718176ec'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.02'))


def downgrade():
    pass
