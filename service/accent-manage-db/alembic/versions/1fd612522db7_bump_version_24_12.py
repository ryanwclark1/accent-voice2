"""bump_version_24_12

Revision ID: 1fd612522db7
Revises: 439de3c2f1ae

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '1fd612522db7'
down_revision = '439de3c2f1ae'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.12'))


def downgrade():
    pass
