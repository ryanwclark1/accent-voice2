"""remove_pickupmember_invalid

Revision ID: 378c46e8c6fe
Revises: 58fc78d9f67f

"""

from sqlalchemy import sql

from alembic import op

# revision identifiers, used by Alembic.
revision = '378c46e8c6fe'
down_revision = '58fc78d9f67f'

userfeatures = sql.table(
    'userfeatures',
    sql.column('id'),
)

groupfeatures = sql.table(
    'groupfeatures',
    sql.column('id'),
)

queuefeatures = sql.table(
    'queuefeatures',
    sql.column('id'),
)

pickupmember = sql.table(
    'pickupmember',
    sql.column('membertype'),
    sql.column('memberid'),
)


def upgrade():
    conn = op.get_bind()
    group_ids = [r.id for r in conn.execute(sql.select([groupfeatures.c.id])).fetchall()]
    queue_ids = [r.id for r in conn.execute(sql.select([queuefeatures.c.id])).fetchall()]
    user_ids = [r.id for r in conn.execute(sql.select([userfeatures.c.id])).fetchall()]

    filters = []
    if group_ids:
        filters.append(
            sql.and_(
                pickupmember.c.membertype == 'group',
                sql.not_(pickupmember.c.memberid.in_(group_ids)),
            )
        )
    if queue_ids:
        filters.append(
            sql.and_(
                pickupmember.c.membertype == 'queue',
                sql.not_(pickupmember.c.memberid.in_(queue_ids)),
            ),
        )
    if user_ids:
        filters.append(
            sql.and_(
                pickupmember.c.membertype == 'user',
                sql.not_(pickupmember.c.memberid.in_(user_ids)),
            ),
        )

    if filters:
        op.execute(
            pickupmember
            .delete()
            .where(sql.or_(*filters))
        )


def downgrade():
    pass
