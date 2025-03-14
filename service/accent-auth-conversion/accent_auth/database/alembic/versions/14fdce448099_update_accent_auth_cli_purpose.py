"""update-accent-auth-cli-purpose

Revision ID: 14fdce448099
Revises: 7386d3b3e545

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '14fdce448099'
down_revision = '7386d3b3e545'

user = sa.sql.table('auth_user', sa.Column('username'), sa.Column('purpose'))

USERNAME = 'accent-auth-cli'
NEW_PURPOSE = 'internal'
OLD_PURPOSE = 'user'


def upgrade():
    _update_purpose(NEW_PURPOSE)


def downgrade():
    _update_purpose(OLD_PURPOSE)


def _update_purpose(purpose):
    query = user.update().values(purpose=purpose).where(user.c.username == USERNAME)
    op.execute(query)
