"""bump_version_22_03

Revision ID: 5863384621a1
Revises: 3314b25783a2

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '5863384621a1'
down_revision = '3314b25783a2'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.03'))


def downgrade():
    pass
