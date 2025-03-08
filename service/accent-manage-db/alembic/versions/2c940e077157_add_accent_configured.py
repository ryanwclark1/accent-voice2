"""add_accent_configured

Revision ID: 2c940e077157
Revises: 2ba2f1d009ca

"""

from sqlalchemy import Column, sql
from sqlalchemy.types import Boolean

from alembic import op

# revision identifiers, used by Alembic.
revision = '2c940e077157'
down_revision = '2ba2f1d009ca'

general = sql.table('general',
                    sql.column('configured'))


def upgrade():
    op.add_column('general',
                  Column('configured',
                         Boolean,
                         nullable=False,
                         server_default='False'))

    op.execute(general
               .update()
               .values(configured=True))


def downgrade():
    op.drop_column('general', 'configured')
