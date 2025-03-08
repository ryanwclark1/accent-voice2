"""bump_version_24_08

Revision ID: 65b4ba443641
Revises: 32101258dffb

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '65b4ba443641'
down_revision = '32101258dffb'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.08'))


def downgrade():
    pass
