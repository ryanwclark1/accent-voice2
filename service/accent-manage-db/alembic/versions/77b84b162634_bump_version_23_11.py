"""bump_version_23_11

Revision ID: 77b84b162634
Revises: b4fb4eb3cf8e

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '77b84b162634'
down_revision = 'b4fb4eb3cf8e'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.11'))


def downgrade():
    pass
