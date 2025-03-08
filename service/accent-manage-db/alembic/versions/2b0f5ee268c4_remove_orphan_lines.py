"""remove orphan lines

Revision ID: 2b0f5ee268c4
Revises: 3133fb4958ef

"""

# revision identifiers, used by Alembic.
revision = '2b0f5ee268c4'
down_revision = '3133fb4958ef'

from sqlalchemy import sql

from alembic import op

linefeatures_table = sql.table('linefeatures',
                               sql.column('id'),
                               sql.column('protocol'),
                               sql.column('protocolid'),
                               sql.column('device'))
user_line_table = sql.table('user_line',
                            sql.column('line_id'))


def upgrade():
    op.execute(linefeatures_table
               .delete()
               .where(
                    sql.and_(
                        linefeatures_table.c.protocol == None,
                        linefeatures_table.c.protocolid == None,
                        linefeatures_table.c.id.notin_(sql.select([user_line_table.c.line_id])))
                ))


def downgrade():
    pass
