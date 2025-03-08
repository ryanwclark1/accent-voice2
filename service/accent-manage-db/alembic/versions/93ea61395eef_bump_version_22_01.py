"""bump_version_22_01

Revision ID: 93ea61395eef
Revises: 29290c38946f

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '93ea61395eef'
down_revision = '29290c38946f'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.01'))


def downgrade():
    pass
