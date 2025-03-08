"""fix_jitter_buffer_implementation_choice

Revision ID: 5c8dc069cfd7
Revises: 425eebc346b1

"""

# revision identifiers, used by Alembic.
revision = '5c8dc069cfd7'
down_revision = '425eebc346b1'

from sqlalchemy import sql

from alembic import op

staticsip = sql.table('staticsip',
                      sql.column('var_name'),
                      sql.column('var_val'))


def upgrade():
    query = (staticsip
             .update()
             .values(var_val='adaptive')
             .where(sql.and_(
                 staticsip.c.var_name == "jbimpl",
                 staticsip.c.var_val == "adaptative")))
    op.execute(query)


def downgrade():
    pass
