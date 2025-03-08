"""enable starttls

Revision ID: 503cf85083ba
Revises: 57a7c7438b98

"""

# revision identifiers, used by Alembic.
revision = '503cf85083ba'
down_revision = '57a7c7438b98'

from sqlalchemy import sql

from alembic import op

cti_main_table = sql.table('ctimain', sql.column('ctis_active'))


def upgrade():
    op.execute(cti_main_table.update().values(ctis_active=1))


def downgrade():
    pass
