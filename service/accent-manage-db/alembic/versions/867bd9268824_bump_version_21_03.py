"""bump_version_21_03

Revision ID: 867bd9268824
Revises: e5281e98b300

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '867bd9268824'
down_revision = 'e5281e98b300'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.03'))


def downgrade():
    pass
