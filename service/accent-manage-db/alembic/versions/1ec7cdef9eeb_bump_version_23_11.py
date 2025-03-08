"""bump-version-23-11

Revision ID: 1ec7cdef9eeb
Revises: 898154753a9b

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '1ec7cdef9eeb'
down_revision = '898154753a9b'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.11'))


def downgrade():
    pass
