"""bump_version_23_15

Revision ID: bcc124448097
Revises: 9ce1ffce9f15

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'bcc124448097'
down_revision = '9ce1ffce9f15'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.15'))


def downgrade():
    pass
