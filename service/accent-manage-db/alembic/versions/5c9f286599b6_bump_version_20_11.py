"""bump_version_20_11

Revision ID: 5c9f286599b6
Revises: f055e37e6196

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '5c9f286599b6'
down_revision = 'f055e37e6196'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.11'))


def downgrade():
    pass
