#!/usr/bin/env bash

# Base path for all services
BASE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../service" && pwd)"

# all python packages, in topological order
SERVICES='
accent-agentd
accent-agentd-cli
accent-agid
accent-amid
accent-auth
accent-auth-cli
accent-call-logd
accent-calld
accent-certs
accent-chatd
accent-confd
accent-confd-cli
accent-confgend
accent-debug
accent-dird
accent-export-import
accent-manage-db
accent-phoned
accent-plugind
accent-plugind-cli
accent-prometheus-exporter-plugin
accent-provd
accent-provd-cli
accent-provd-plugins
accent-purge-db
accent-setupd
accent-stat
accent-ui
accent-webhookd
accent-websocketd
'

# Function to convert SERVICE string into an array with full paths
get_service_with_paths() {
    local service_with_paths=()
    while read -r service; do
        # Skip empty lines
        [[ -z "$service" ]] && continue
        service_with_paths+=("${BASE_PATH}/${service}")
    done <<< "$SERVICES"
    echo "${service_with_paths[@]}"
}

get_service_with_paths