#!/usr/bin/env bash


# Base path for all libraries
BASE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../library" && pwd)"

# all python packages, in topological order
LIBRARIES='
accent-agentd-client
accent-amid-client
accent-asterisk-doc-extractor
accent-asyncio-ari-client
accent-auth-client
accent-auth-keys
accent-bus
accent-call-logd-client
accent-calld-client
accent-confd-client
accent-confgend-client
accent-config
accent-dao
accent-deployd-client
accent-dird-client
accent-fetchfw
accent-lib-python
accent-lib-rest-client
accent-market-client
accent-plugind-client
accent-provd-client
accent-setupd-client
accent-test-helpers
accent-uuid
accent-webhookd-client
accent-websocketd-client
ari-py
swagger-py
'

get_library_with_paths() {
    local library_with_paths=()
    while read -r library; do
        # Skip empty lines
        [[ -z "$library" ]] && continue
        library_with_paths+=("${BASE_PATH}/${library}")
    done <<< "$LIBRARIES"
    echo "${library_with_paths[@]}"
}

get_library_with_paths