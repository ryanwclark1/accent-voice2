"""bump_version_19_04

Revision ID: 3f132402532b
Revises: 1a13acc6cdb0

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '3f132402532b'
down_revision = '1a13acc6cdb0'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.04'))


def downgrade():
    pass
