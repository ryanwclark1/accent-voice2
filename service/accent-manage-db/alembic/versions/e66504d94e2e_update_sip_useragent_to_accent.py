"""update_sip_useragent_to_accent

Revision ID: e66504d94e2e
Revises: 1a72b3da2baf

"""

# revision identifiers, used by Alembic.
revision = 'e66504d94e2e'
down_revision = '1a72b3da2baf'

from sqlalchemy import func, sql

from alembic import op

staticsip = sql.table('staticsip',
                      sql.column('var_name'),
                      sql.column('var_val'))


def upgrade():
    query = (staticsip
             .update()
             .values(var_val='Accent PBX')
             .where(sql.and_(
                 staticsip.c.var_name == "useragent",
                 func.lower(staticsip.c.var_val) == "accent pbx")))
    op.execute(query)


def downgrade():
    query = (staticsip
             .update()
             .values(var_val='Accent PBX')
             .where(sql.and_(
                 staticsip.c.var_name == "useragent",
                 func.lower(staticsip.c.var_val) == "accent pbx")))
    op.execute(query)
