"""bump_version_19_15

Revision ID: 732a9b6500da
Revises: 5faf5386dca8

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '732a9b6500da'
down_revision = '5faf5386dca8'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.15'))


def downgrade():
    pass
