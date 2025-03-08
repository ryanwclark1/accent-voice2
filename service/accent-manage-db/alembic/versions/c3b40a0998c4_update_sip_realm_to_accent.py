"""update_sip_realm_to_accent

Revision ID: c3b40a0998c4
Revises: 30d7dcbb9133

"""

# revision identifiers, used by Alembic.
revision = 'c3b40a0998c4'
down_revision = '30d7dcbb9133'

from sqlalchemy import func, sql

from alembic import op

staticsip = sql.table('staticsip',
                      sql.column('var_name'),
                      sql.column('var_val'))


def upgrade():
    query = (staticsip
             .update()
             .values(var_val='accent')
             .where(sql.and_(
                 staticsip.c.var_name == "realm",
                 func.lower(staticsip.c.var_val) == "accent")))
    op.execute(query)


def downgrade():
    query = (staticsip
             .update()
             .values(var_val='accent')
             .where(sql.and_(
                 staticsip.c.var_name == "realm",
                 func.lower(staticsip.c.var_val) == "accent")))
    op.execute(query)
