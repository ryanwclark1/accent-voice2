import os
import psycopg2
import subprocess

from pprint import pprint
from pwd import getpwnam


def run_as(user_name):
    def wrapper(f):
        def decorator(*args, **kwargs):
            starting_uid = os.geteuid()
            user = getpwnam(user_name)
            os.seteuid(user.pw_uid)
            res = f(*args, **kwargs)
            os.seteuid(starting_uid)
            return res
        return decorator
    return wrapper


@run_as('postgres')
def list_pg_connections():
    conn = psycopg2.connect('postgresql:///postgres')
    cur = conn.cursor()

    cur.execute("SELECT pid,client_addr,client_port,query FROM pg_stat_activity WHERE state = 'idle in transaction';")

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results


def main():
    '''
    Lists PG connections that are "idle in transation", meaning stuck in a
    transaction that was neither committed or rollbacked. See bug #6607 for what
    this script is trying to detect.
    '''

    for pg_pid, client_addr, client_port, query in list_pg_connections():
        pids = subprocess.check_output(['lsof', '-ti', 'tcp@{host}:{port}'.format(host=client_addr, port=client_port)]).strip()
        client_pid = next(pid for pid in pids.split('\n') if pid != pg_pid)
        client_command = subprocess.check_output(['ps', '-p', str(client_pid), '-o', 'cmd', 'h']).strip()

        pprint({'process': client_command,
                'SQL query': query})
        print '---------------'


if __name__ == '__main__':
    main()
