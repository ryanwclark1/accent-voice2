"""bump_version_18_02

Revision ID: 2991705be1ec
Revises: 18840b2fdb03

"""

# revision identifiers, used by Alembic.
revision = '2991705be1ec'
down_revision = '18840b2fdb03'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.02'))


def downgrade():
    pass
