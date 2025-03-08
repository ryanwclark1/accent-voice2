"""bump_version_22_04

Revision ID: 0ffacfab7041
Revises: 5863384621a1

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0ffacfab7041'
down_revision = '5863384621a1'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.04'))


def downgrade():
    pass
