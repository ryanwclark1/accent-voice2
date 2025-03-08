"""bump_version_17_07

Revision ID: 42e9771685b0
Revises: 596b177ba681

"""

# revision identifiers, used by Alembic.
revision = '42e9771685b0'
down_revision = '596b177ba681'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.07'))


def downgrade():
    pass
