"""bump_version_20_08

Revision ID: 7d91d22133a9
Revises: 2a27e01c8070

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '7d91d22133a9'
down_revision = '2a27e01c8070'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.08'))


def downgrade():
    pass
