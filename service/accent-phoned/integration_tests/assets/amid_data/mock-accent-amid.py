# Copyright 2023 Accent Communications

import json
import logging
import sys

from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

action_response = ''
valid_extens = []
_requests = []


def _reset():
    global _requests
    global action_response
    global valid_extens
    _requests = []
    action_response = ''
    valid_extens = []


@app.before_request
def log_request():
    global _requests

    if request.path.startswith('/_'):
        return

    log = {
        'method': request.method,
        'path': request.path,
        'query': dict(request.args.items(multi=True)),
        'body': request.data.decode('utf-8'),
        'json': request.json if request.is_json else None,
        'headers': dict(request.headers),
    }
    _requests.append(log)


@app.route('/_reset', methods=['POST'])
def reset():
    _reset()
    return '', 204


@app.route('/_requests', methods=['GET'])
def list_requests():
    return jsonify({'requests': _requests})


@app.route("/_set_action", methods=['POST'])
def set_action():
    global action_response
    action_response = request.get_json()

    return '', 204


@app.route("/1.0/action/<action>", methods=['POST'])
def action(action):
    return json.dumps(action_response), 200


if __name__ == "__main__":
    port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port, debug=True)
