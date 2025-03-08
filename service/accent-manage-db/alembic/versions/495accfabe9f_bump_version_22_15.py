"""bump_version_22_15

Revision ID: 495accfabe9f
Revises: 7d342adb6ae1

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '495accfabe9f'
down_revision = '7d342adb6ae1'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.15'))


def downgrade():
    pass
