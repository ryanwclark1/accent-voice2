#!/bin/bash
# Copyright 2023 Accent Communications

set -e
set -u  # fail if variable is undefined
set -o pipefail  # fail if command before pipe fails

# RESOURCES_FILENAME="/usr/share/asterisk/rest-api/resources.json"
RESOURCES_FILENAME="/var/lib/asterisk/rest-api/resources.json"

if jq -r '.apis[] .path ' "${RESOURCES_FILENAME}" | grep -q '/api-docs/amqp'; then
    exit 0
fi

patched_resources_filename=$(mktemp)

jq '.apis[.apis | length] |= . + {"path": "/api-docs/amqp.{format}", "description": "AMQP resource"}' "${RESOURCES_FILENAME}" > "${patched_resources_filename}"
chmod 0644 "${patched_resources_filename}"
mv "${patched_resources_filename}" "${RESOURCES_FILENAME}"
