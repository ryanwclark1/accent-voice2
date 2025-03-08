# Copyright 2023 Accent Communications

from accent_auth_client import Client as AuthClient
from accent_confd_client import Client as ConfdClient

HOST = 'accent-dev'
USERNAME = 'test'
PASSWORD = 'test'
AUTH_BACKEND = 'accent_service'
TOKEN_EXPIRATION = 3600
N = 1000
FIRST_EXTEN = 11000
CONTEXT = 'inside'
FIRSTNAME_PREFIX = 'ZZZZZ'


def main():
    auth_client = AuthClient(HOST, username=USERNAME, password=PASSWORD, verify_certificate=False)
    token = auth_client.token.new(AUTH_BACKEND, expiration=TOKEN_EXPIRATION)['token']
    confd_client = ConfdClient(HOST, token=token, verify_certificate=False)
    for i in range(N):
        user_data = dict(
            firstname=' '.join([FIRSTNAME_PREFIX, str(i)]),
        )
        exten_data = dict(
            exten=str(FIRST_EXTEN + i),
            context=CONTEXT,
        )

        print('Creating ', user_data, '...')
        user = confd_client.users.create(user_data)
        exten = confd_client.extensions.create(exten_data)
        line = confd_client.lines_sip.create({'context': CONTEXT})

        confd_client.users(user).add_line(line)
        confd_client.lines(line).add_extension(exten)


if __name__ == '__main__':
    main()
