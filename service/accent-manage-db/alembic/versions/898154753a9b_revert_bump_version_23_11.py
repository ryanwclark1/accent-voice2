"""revert-bump-version-23-11

Revision ID: 898154753a9b
Revises: 74818b4464a1

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '898154753a9b'
down_revision = '74818b4464a1'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.10'))


def downgrade():
    pass
