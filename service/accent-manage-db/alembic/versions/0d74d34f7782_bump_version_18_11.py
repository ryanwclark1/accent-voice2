"""bump_version_18_11

Revision ID: 0d74d34f7782
Revises: 47920341f392

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0d74d34f7782'
down_revision = '47920341f392'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.11'))


def downgrade():
    pass
