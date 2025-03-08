"""bump_version_24_13

Revision ID: b9653254a483
Revises: 1fd612522db7

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b9653254a483'
down_revision = '1fd612522db7'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.13'))


def downgrade():
    pass
