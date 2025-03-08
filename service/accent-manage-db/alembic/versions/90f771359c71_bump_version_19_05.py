"""bump_version_19_05

Revision ID: 90f771359c71
Revises: 454c3dfde5db

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '90f771359c71'
down_revision = '454c3dfde5db'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.05'))


def downgrade():
    pass
