"""bump_version_17_05

Revision ID: 19a869176d6c
Revises: 37b9ac945437

"""

# revision identifiers, used by Alembic.
revision = '19a869176d6c'
down_revision = '37b9ac945437'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.05'))


def downgrade():
    pass
