"""remove chan_sip permaturemedia

Revision ID: 3f310bfa7f9a
Revises: 2989b8b30fe7

"""

# revision identifiers, used by Alembic.
revision = '3f310bfa7f9a'
down_revision = '2989b8b30fe7'

from sqlalchemy import sql

from alembic import op

staticsip = sql.table('staticsip',
                      sql.column('var_name'))


def upgrade():
    op.execute(staticsip.delete().where(staticsip.c.var_name == 'permaturemedia'))


def downgrade():
    pass
