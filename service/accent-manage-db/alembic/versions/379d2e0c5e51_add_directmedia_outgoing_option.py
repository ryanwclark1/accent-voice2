"""add directmedia outgoing option

Revision ID: 379d2e0c5e51
Revises: 1888ca44e08f

"""

import sqlalchemy as sa
from sqlalchemy import sql

from alembic import op

revision = '379d2e0c5e51'
down_revision = '1888ca44e08f'


old_options = ('no', 'yes', 'nonat', 'update', 'update,nonat')

old_type = sa.Enum(*old_options, name='usersip_directmedia')

usersip_table = sa.sql.table('usersip',
                             sql.column('directmedia'))

staticsip_table = sa.sql.table('staticsip',
                               sql.column('var_name'),
                               sql.column('var_val'))


def upgrade():
    op.alter_column('usersip', 'directmedia', type_=sa.String(20))

    op.create_check_constraint(
        "usersip_directmedia_check",
        "usersip",
        usersip_table.c.directmedia.in_(
            ['no', 'yes', 'nonat', 'update', 'update,nonat', 'outgoing'])
    )

    old_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    op.execute(usersip_table.update().
               where(usersip_table.c.directmedia == 'outgoing').
               values(directmedia='no'))

    op.execute(staticsip_table.update().
               where(sa.sql.and_(
                   staticsip_table.c.var_name == 'directmedia',
                   staticsip_table.c.var_val == 'outgoing')).
               values(var_val='no'))

    op.drop_constraint('usersip_directmedia_check', 'usersip')

    old_type.create(op.get_bind(), checkfirst=False)

    qry = """
    ALTER TABLE usersip
    ALTER COLUMN directmedia
    TYPE usersip_directmedia
    USING (directmedia::usersip_directmedia);
    """
    op.execute(qry)
