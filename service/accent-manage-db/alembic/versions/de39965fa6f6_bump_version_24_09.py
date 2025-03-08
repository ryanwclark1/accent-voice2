"""bump_version_24_09

Revision ID: de39965fa6f6
Revises: a805579d911f

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'de39965fa6f6'
down_revision = 'a805579d911f'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.09'))


def downgrade():
    pass
