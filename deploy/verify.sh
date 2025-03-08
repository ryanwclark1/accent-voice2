#!/bin/bash

set -e
set -u  # fail if variable is undefined
set -o pipefail  # fail if command before pipe fails

function wait_for_bootstrap_complete() {
    seconds=0
    timeout=120
    echo -n 'Waiting for bootstrap complete'
    while [ "$seconds" -lt "$timeout" ] && [ "$(docker compose ps --all --format json bootstrap | jq --raw-output .State)" != 'exited' ];
      do
        echo -n '.'
        seconds=$((seconds+2))
        sleep 2
      done

    if [ "$seconds" -ge "$timeout" ]; then
        echo ' Timeout!'
        exit 1
    fi

    echo ' Ready!'
}

wait_for_bootstrap_complete

echo -n 'Validating bootstrap exit status... '
BOOTSTRAP_EXIT_CODE=$(docker compose ps --all --status exited --format json bootstrap | jq --raw-output .ExitCode)
if [ "$BOOTSTRAP_EXIT_CODE" -ne 0 ]; then
    echo 'FAILED'
    exit 1
fi
echo 'SUCCEED'

echo -n 'Creating token... '
RESULT=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --basic \
  --user "root:secret" \
  -d '{}' \
  'https://api.accentvoice.io/api/auth/0.1/token')
echo $RESULT
TOKEN=$(echo $RESULT | jq --raw-output .data.token)
echo $TOKEN

echo -n 'Validating accent-auth status... '
AUTH_CODE=$(curl \
  --insecure \
  --silent \
  --show-error \
  --head \
  --output /dev/null \
  --write-out "%{http_code}" \
  'https://api.accentvoice.io/api/auth/0.1/status')

if [ "$AUTH_CODE" -ne 200 ]; then
  echo 'FAILED'
  exit 1
fi
echo 'SUCCEED'

echo -n 'Validating accent-provd status... '
PROVD_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/vnd.accent.provd+json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/provd/0.2/status')

if [ "$(echo $PROVD_STATUS | jq --raw-output .rest_api)" != 'ok' ]; then
  echo 'FAILED'
  exit 1
fi
echo 'SUCCEED'

echo -n 'Validating accent-webhookd status... '
WEBHOOKD_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/webhookd/1.0/status')

if [ "$(echo $WEBHOOKD_STATUS | jq --raw-output .bus_consumer.status)" != 'ok' ]; then
  echo 'FAILED (bus_consume)'
  exit 1
fi
if [ "$(echo $WEBHOOKD_STATUS | jq --raw-output .master_tenant.status)" != 'ok' ]; then
  echo 'FAILED (master_tenant)'
  exit 1
fi
echo "SUCCEED"

echo -n 'Validating accent-dird status... '
DIRD_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/dird/0.1/status')

if [ "$(echo $DIRD_STATUS | jq --raw-output .bus_consumer.status)" != 'ok' ]; then
  echo 'FAILED (bus_consume)'
  exit 1
fi
if [ "$(echo $DIRD_STATUS | jq --raw-output .rest_api.status)" != 'ok' ]; then
  echo 'FAILED (rest_api)'
  exit 1
fi
echo "SUCCEED"

function wait_for_accent_amid_asterisk_connection() {
    seconds=0
    timeout=120
    echo -n 'Waiting for accent-amid asterisk connection'
    while [ "$seconds" -lt "$timeout" ] && [ "$(curl --insecure --silent --request POST --output /dev/null --write-out "%{http_code}" --header 'Content-type: application/json' --header 'Accept: application/json' --header "X-Auth-Token: $TOKEN" 'https://api.accentvoice.io/api/amid/1.0/action/ping')" -eq 503 ];
      do
        echo -n '.'
        seconds=$((seconds+2))
        sleep 2
      done

    echo ' Ready!'
}

wait_for_accent_amid_asterisk_connection
echo -n 'Validating accent-amid status... '
AMID_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request POST \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/amid/1.0/action/ping')

if [ "$(echo $AMID_STATUS | jq --raw-output .[].Response)" != 'Success' ]; then
  echo 'FAILED (ping action)'
  exit 1
fi
echo "SUCCEED"

echo -n 'Validating accent-call-logd status... '
CALL_LOGD_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/call-logd/1.0/status')

if [ "$(echo $CALL_LOGD_STATUS | jq --raw-output .bus_consumer.status)" != 'ok' ]; then
  echo 'FAILED (bus_consume)'
  exit 1
fi
if [ "$(echo $CALL_LOGD_STATUS | jq --raw-output .task_queue.status)" != 'ok' ]; then
  echo 'FAILED (task_queue)'
  # exit 1
fi
if [ "$(echo $CALL_LOGD_STATUS | jq --raw-output .service_token.status)" != 'ok' ]; then
  echo 'FAILED (service_token)'
  exit 1
fi
echo "SUCCEED"

function wait_for_accent_chatd_presence_initialization() {
    seconds=0
    timeout=120
    echo -n 'Waiting for accent-chatd presence initialization complete'
    while [ "$seconds" -lt "$timeout" ] && [ "$(curl --insecure --silent --show-error --request GET --header 'Accept: application/json' --header "X-Auth-Token: $TOKEN" 'https://api.accentvoice.io/api/chatd/1.0/status' | jq --raw-output .presence_initialization.status)" != 'ok' ];
      do
        echo -n '.'
        seconds=$((seconds+2))
        sleep 2
      done

    if [ "$seconds" -ge "$timeout" ]; then
        echo ' Timeout!'
        exit 1
    fi

    echo ' Ready!'
}

wait_for_accent_chatd_presence_initialization
echo -n 'Validating accent-chatd status... '
CHATD_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/chatd/1.0/status')

if [ "$(echo $CHATD_STATUS | jq --raw-output .bus_consumer.status)" != 'ok' ]; then
  echo 'FAILED (bus_consume)'
  exit 1
fi
if [ "$(echo $CHATD_STATUS | jq --raw-output .rest_api.status)" != 'ok' ]; then
  echo 'FAILED (rest_api)'
  exit 1
fi
if [ "$(echo $CHATD_STATUS | jq --raw-output .presence_initialization.status)" != 'ok' ]; then
  echo 'FAILED (presence_initialization)'
  exit 1
fi
if [ "$(echo $CHATD_STATUS | jq --raw-output .master_tenant.status)" != 'ok' ]; then
  echo 'FAILED (master_tenant)'
  exit 1
fi
echo "SUCCEED"

echo -n 'Validating accent-phoned status... '
PHONED_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/phoned/0.1/status')

if [ "$(echo $PHONED_STATUS | jq --raw-output .bus_consumer.status)" != 'ok' ]; then
  echo 'FAILED (bus_consume)'
  exit 1
fi
if [ "$(echo $PHONED_STATUS | jq --raw-output .service_token.status)" != 'ok' ]; then
  echo 'FAILED (service_token)'
  exit 1
fi
echo "SUCCEED"

echo -n 'Validating accent-websocketd status... '
set +e
# NOTE: curl will exit with error code 52 (empty response from server)
WEBSOCKETD_CODE=$(curl \
  --insecure \
  --silent \
  --request GET \
  --head \
  --header 'Host: api.accentvoice.io' \
  --header 'Upgrade: websocket' \
  --header 'Sec-WebSocket-Version: 13' \
  --header 'Sec-WebSocket-Key: 0000000000000000000000==' \
  --output /dev/null \
  --write-out "%{http_code}" \
  "https://api.accentvoice.io/api/websocketd/?token=$TOKEN&version=2")
set -e

if [ "$WEBSOCKETD_CODE" -ne 101 ]; then
  echo 'FAILED'
  echo "WEBSOCKETD_CODE: $WEBSOCKETD_CODE"
  # exit 1
fi
echo "SUCCEED"

echo -n 'Validating accent-calld status... '
CALLD_STATUS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/calld/1.0/status')

if [ "$(echo $CALLD_STATUS | jq --raw-output .ari.status)" != 'ok' ]; then
  echo 'FAILED (ari)'
  # exit 1
fi
if [ "$(echo $CALLD_STATUS | jq --raw-output .bus_consumer.status)" != 'ok' ]; then
  echo 'FAILED (bus_consumer)'
  exit 1
fi
if [ "$(echo $CALLD_STATUS | jq --raw-output .service_token.status)" != 'ok' ]; then
  echo 'FAILED (service_token)'
  exit 1
fi
echo "SUCCEED"

echo -n 'Validating accent-agentd status... '
AGENTD_CODE=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header "X-Auth-Token: $TOKEN" \
  --output /dev/null \
  --write-out "%{http_code}" \
  'https://api.accentvoice.io/api/agentd/1.0/agents')

if [ "$AGENTD_CODE" -ne 200 ]; then
  echo 'FAILED'
  exit 1
fi
echo "SUCCEED"

echo -n 'Validating accent-plugind status... '
echo "WON'T BE IMPLEMENTED"

echo -n 'Validating accent-setupd status... '
echo "WON'T BE IMPLEMENTED"

echo -n 'Getting /api/confd/1.1/users... '
USERS=$(curl \
  --insecure \
  --silent \
  --show-error \
  --request GET \
  --header 'Accept: application/json' \
  --header "X-Auth-Token: $TOKEN" \
  'https://api.accentvoice.io/api/confd/1.1/users?recurse=True')
TOTAL_USERS=$(echo $USERS | jq --raw-output .total)
echo "Total: $TOTAL_USERS"