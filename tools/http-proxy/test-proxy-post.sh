#!/bin/bash

proxy="$1"
destination_url="$2"
expected_status="$3"

if [ -z "$proxy" -o -z "$destination_url" -o -z "$expected_status" ] ; then
    echo "Usage: $0 <proxy_host:port> <destination_url> <expected_status>"
    exit 1
fi

export HTTP_PROXY="$proxy"
export HTTPS_PROXY="$proxy"
export NO_PROXY=localhost,127.0.0.1,127.0.1.1

python3 <<EOF
import requests

response = requests.post('$destination_url', data='{}')
if response.status_code == $expected_status:
    print('Proxy OK')
else:
    response.raise_for_status()
EOF
