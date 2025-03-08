"""bump_version_19_07

Revision ID: 7d47aaef973a
Revises: 9b0892a818e6

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '7d47aaef973a'
down_revision = '9b0892a818e6'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.07'))


def downgrade():
    pass
