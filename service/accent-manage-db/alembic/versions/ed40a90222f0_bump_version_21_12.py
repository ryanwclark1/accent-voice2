"""bump_version_21_12

Revision ID: ed40a90222f0
Revises: 56a75d478edc

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'ed40a90222f0'
down_revision = '56a75d478edc'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.12'))


def downgrade():
    pass
