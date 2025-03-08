"""bump_version_21_11

Revision ID: 06e9e3483fec
Revises: 907d4947d665

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '06e9e3483fec'
down_revision = '907d4947d665'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.11'))


def downgrade():
    pass
