"""bump_version_21_05

Revision ID: e6c5e0410e89
Revises: 4d539700bb90

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e6c5e0410e89'
down_revision = '4d539700bb90'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.05'))


def downgrade():
    pass
