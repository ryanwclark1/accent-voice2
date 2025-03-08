"""revert version upgrade

Revision ID: 785b8cb74daa
Revises: 93ea61395eef

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '785b8cb74daa'
down_revision = '93ea61395eef'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.16'))


def downgrade():
    pass
