"""bump_version_23_10

Revision ID: 8fe383847bcc
Revises: 8675398b047b

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '8fe383847bcc'
down_revision = '8675398b047b'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.10'))


def downgrade():
    pass
