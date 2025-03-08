"""bump_version_18_04

Revision ID: 1747774cead4
Revises: 28443bfc4fb1

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '1747774cead4'
down_revision = '28443bfc4fb1'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.04'))


def downgrade():
    pass
