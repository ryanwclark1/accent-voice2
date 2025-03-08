"""bump_version_18_10

Revision ID: 57ab432bb1c3
Revises: 235158681deb

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '57ab432bb1c3'
down_revision = '235158681deb'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.10'))


def downgrade():
    pass
