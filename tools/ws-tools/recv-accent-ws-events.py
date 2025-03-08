import json
import pprint
import ssl
import sys
from getpass import getpass

import websocket
from accent_auth_client import Client

host = sys.argv[1]
username = sys.argv[2]
events = sys.argv[3].split(',')
password = getpass(f'Password for {username}: ')

auth = Client(host, 443, username=username, password=password, verify_certificate=False)
token = auth.token.new(backend='accent_user')['token']


def on_message(ws, message):
    pprint.pprint(json.loads(message))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    for event in events:
        ws.send(json.dumps({"op": "subscribe", "data": {"event_name": event}}))
    ws.send(json.dumps({"op": "start"}))


ws = websocket.WebSocketApp(
    f"wss://{host}:443/api/websocketd/?token={token}",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
ws.on_open = on_open
ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
