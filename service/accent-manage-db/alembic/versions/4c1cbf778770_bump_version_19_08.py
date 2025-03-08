"""bump_version_19_08

Revision ID: 4c1cbf778770
Revises: 15ca57fa1b71

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4c1cbf778770'
down_revision = '15ca57fa1b71'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.08'))


def downgrade():
    pass
