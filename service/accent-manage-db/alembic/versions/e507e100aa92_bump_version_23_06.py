"""bump_version_23_06

Revision ID: e507e100aa92
Revises: aaf16eeecf7f

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e507e100aa92'
down_revision = 'aaf16eeecf7f'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.06'))


def downgrade():
    pass
