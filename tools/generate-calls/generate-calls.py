#!/usr/bin/env python3

from accent_auth_client import Client as Auth
from accent_amid_client import Client as Amid
from time import sleep

server = "localhost"
username = "" # User with good ACL
password = ""
context = "" # Context where you wanted to route the call
number = "" # Number you want to call
expiration = 3600
timeout = 1 # Make call each seconds

########################
# Dialplan needed in /etc/asterisk/extensions_extra.d/test.conf
# [test]
# exten = originate,1,NoOp(Originate test)
# same  =           n,Answer(6000)
# same  =           n,Playback(hello-world)
# same  =           n,Hangup()

#########################
a = Auth(server, username=username, password=password, verify_certificate=False)

t = a.token.new('accent_user', expiration=expiration)
token = t['token']

ami = Amid(server, verify_certificate=False, token=token)

try:
    while True:
        print(f'Call {number}')
        response = ami.action('originate', {
            'Channel': 'Local/originate@test',
            'Exten': number,
            'Context': context,
            'Priority': 1
        })

        if response and response[0].get('Response') == 'Success':
            print(f"{response[0]['Response']} - {response[0]['Message']}")
        else:
            print('Error: Could not make the call.')

        sleep(timeout)

except KeyboardInterrupt:
    print('Loop has been suspended, removing token.')
    a.token.revoke(token)
