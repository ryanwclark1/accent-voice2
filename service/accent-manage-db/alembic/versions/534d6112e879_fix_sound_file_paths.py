"""fix_sound_file_paths

Revision ID: 534d6112e879
Revises: 35a7f7e2dc33

"""

# revision identifiers, used by Alembic.

from sqlalchemy import sql

from alembic import op

revision = '534d6112e879'
down_revision = '35a7f7e2dc33'


schedule = sql.table('schedule',
                     sql.column('fallback_action'),
                     sql.column('fallback_actionid'))

schedule_time = sql.table('schedule_time',
                          sql.column('action'),
                          sql.column('actionid'))

dialaction = sql.table('dialaction',
                       sql.column('action'),
                       sql.column('actionarg1'))


def upgrade():
    fix_queues()
    fix_schedules()
    fix_dialactions()


def fix_queues():
    query = """
    UPDATE
        queue
    SET
        "announce" = replace("announce", 'pf-accent', 'accent'),
        "periodic-announce" = replace("periodic-announce", 'pf-accent', 'accent'),
        "queue-youarenext" = replace("queue-youarenext", 'pf-accent', 'accent'),
        "queue-thereare" = replace("queue-thereare", 'pf-accent', 'accent'),
        "queue-callswaiting" = replace("queue-callswaiting", 'pf-accent', 'accent'),
        "queue-holdtime" = replace("queue-holdtime", 'pf-accent', 'accent'),
        "queue-minutes" = replace("queue-minutes", 'pf-accent', 'accent'),
        "queue-seconds" = replace("queue-seconds", 'pf-accent', 'accent'),
        "queue-thankyou" = replace("queue-thankyou", 'pf-accent', 'accent'),
        "queue-reporthold" = replace("queue-reporthold", 'pf-accent', 'accent')
    WHERE
        announce LIKE '%pf-accent%'
        OR "periodic-announce" LIKE '%pf-accent%'
        OR "queue-youarenext" LIKE '%pf-accent%'
        OR "queue-thereare" LIKE '%pf-accent%'
        OR "queue-callswaiting" LIKE '%pf-accent%'
        OR "queue-holdtime" LIKE '%pf-accent%'
        OR "queue-minutes" LIKE '%pf-accent%'
        OR "queue-seconds" LIKE '%pf-accent%'
        OR "queue-thankyou" LIKE '%pf-accent%'
        OR "queue-reporthold" LIKE '%pf-accent%'
    """

    op.execute(query)


def fix_schedules():
    schedule_query = (schedule.update()
                      .where(
                          sql.and_(schedule.c.fallback_action == 'sound',
                                   schedule.c.fallback_actionid.like('%pf-accent%')))
                      .values(fallback_actionid=sql.func.replace(schedule.c.fallback_actionid,
                                                                 'pf-accent',
                                                                 'accent')))

    schedule_time_query = (schedule_time.update()
                           .where(
                               sql.and_(schedule_time.c.action == 'sound',
                                        schedule_time.c.actionid.like('%pf-accent%')))
                           .values(actionid=sql.func.replace(schedule_time.c.actionid,
                                                             'pf-accent',
                                                             'accent')))

    op.execute(schedule_query)
    op.execute(schedule_time_query)


def fix_dialactions():
    query = (dialaction.update()
             .where(
                 sql.and_(dialaction.c.action == 'sound',
                          dialaction.c.actionarg1.like('%pf-accent%')))
             .values(actionarg1=sql.func.replace(dialaction.c.actionarg1,
                                                 'pf-accent',
                                                 'accent')))

    op.execute(query)


def downgrade():
    unfix_queues()
    unfix_schedules()
    unfix_dialactions()


def unfix_queues():
    query = """
    UPDATE
        queue
    SET
        "announce" = replace("announce", '/accent/', '/pf-accent/'),
        "periodic-announce" = replace("periodic-announce", '/accent/', '/pf-accent/'),
        "queue-youarenext" = replace("queue-youarenext", '/accent/', '/pf-accent/'),
        "queue-thereare" = replace("queue-thereare", '/accent/', '/pf-accent/'),
        "queue-callswaiting" = replace("queue-callswaiting", '/accent/', '/pf-accent/'),
        "queue-holdtime" = replace("queue-holdtime", '/accent/', '/pf-accent/'),
        "queue-minutes" = replace("queue-minutes", '/accent/', '/pf-accent/'),
        "queue-seconds" = replace("queue-seconds", '/accent/', '/pf-accent/'),
        "queue-thankyou" = replace("queue-thankyou", '/accent/', '/pf-accent/'),
        "queue-reporthold" = replace("queue-reporthold", '/accent/', '/pf-accent/')
    WHERE
        "announce" LIKE '%/accent/%'
        OR "periodic-announce" LIKE '%/accent/%'
        OR "queue-youarenext" LIKE '%/accent/%'
        OR "queue-thereare" LIKE '%/accent/%'
        OR "queue-callswaiting" LIKE '%/accent/%'
        OR "queue-holdtime" LIKE '%/accent/%'
        OR "queue-minutes" LIKE '%/accent/%'
        OR "queue-seconds" LIKE '%/accent/%'
        OR "queue-thankyou" LIKE '%/accent/%'
        OR "queue-reporthold" LIKE '%/accent/%'
    """

    op.execute(query)


def unfix_schedules():
    schedule_query = (schedule.update()
                      .where(
                          sql.and_(schedule.c.fallback_action == 'sound',
                                   schedule.c.fallback_actionid.like('%/accent/%')))
                      .values(fallback_actionid=sql.func.replace(schedule.c.fallback_actionid,
                                                                 '/accent/',
                                                                 '/pf-accent/')))

    schedule_time_query = (schedule_time.update()
                           .where(
                               sql.and_(schedule_time.c.action == 'sound',
                                        schedule_time.c.actionid.like('%/accent/%')))
                           .values(actionid=sql.func.replace(schedule_time.c.actionid,
                                                             '/accent/',
                                                             '/pf-accent/')))

    op.execute(schedule_query)
    op.execute(schedule_time_query)


def unfix_dialactions():
    query = (dialaction.update()
             .where(
                 sql.and_(dialaction.c.action == 'sound',
                          dialaction.c.actionarg1.like('%/accent/%')))
             .values(actionarg1=sql.func.replace(dialaction.c.actionarg1,
                                                 '/accent/',
                                                 '/pf-accent/')))

    op.execute(query)
