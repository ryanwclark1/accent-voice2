"""bump_version_18_05

Revision ID: 52acaaba550c
Revises: 4a5a1c3eb52f

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '52acaaba550c'
down_revision = '4a5a1c3eb52f'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.05'))


def downgrade():
    pass
