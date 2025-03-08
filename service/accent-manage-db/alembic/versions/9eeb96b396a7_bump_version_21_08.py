"""bump_version_21_08

Revision ID: 9eeb96b396a7
Revises: 2b5d68fa7ab8

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '9eeb96b396a7'
down_revision = '2b5d68fa7ab8'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.08'))


def downgrade():
    pass
