#!/bin/sh

# all python packages with dockerfile, in topological order
SERVICES=(
    "accent-agentd"
    "accent-agid"
    "accent-amid"
    "accent-auth"
    "accent-auth-cli"
    "accent-call-logd"
    "accent-calld"
    "accent-chatd"
    "accent-confd"
    "accent-confd-cli"
    "accent-confgend"
    "accent-dird"
    "accent-manage-db"
    "accent-phoned"
    "accent-plugind"
    "accent-provd"
    # "accent-rtpe-config"
    "accent-setupd"
    "accent-ui"
    "accent-webhookd"
    "accent-websocketd"
)
