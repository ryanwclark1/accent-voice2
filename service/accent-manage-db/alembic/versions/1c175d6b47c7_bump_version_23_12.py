"""bump_version_23_12

Revision ID: 1c175d6b47c7
Revises: 1ec7cdef9eeb

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '1c175d6b47c7'
down_revision = '1ec7cdef9eeb'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.12'))


def downgrade():
    pass
