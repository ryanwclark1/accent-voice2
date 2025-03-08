"""bump_version_17_02

Revision ID: 8c21acf4e9e
Revises: 196dea1085af

"""

# revision identifiers, used by Alembic.
revision = '8c21acf4e9e'
down_revision = '196dea1085af'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.02'))


def downgrade():
    pass
