#!/bin/bash

# Small script which can be used to massively restart, remove local conf or reset Aastra phones
# Usage :
#   aastra_sipphones_reset.sh IP1[,IP2[,...]] [ACTION]
#
# ACTION is one of :
#  restart : restart phones
#  local   : remove local configuration
#  factory : reset phone to factory configuration

AASTRA_LOGIN="admin"
AASTRA_PASSWD="22222"
AASTRA_ACTION="restart" # Default action
if [ $# -lt 1 ]; then
    echo -e "ERROR: missing mandatory args
            usage: $0 IP1[,IP2[,...]] [ACTION]
            where
                IP1,IP2 is a comma separated IP list
                ACTION is to be chosen between restart, local and factory (default: restart)"
    exit 1
elif [ $# -eq 1 ]; then
    OIFS=${IFS}
    IFS=','          # Change IFS to ',' to make AASTRA_IP an array of IP
    AASTRA_IP=(${1}) # Make an array of IP
    IFS=${OIFS}
elif [ $# -eq 2 ]; then
    AASTRA_ACTION="$2"
    OIFS=${IFS}
    IFS=','          # Change IFS to ',' to make AASTRA_IP an array of IP
    AASTRA_IP=(${1}) # Make an array of IP
    IFS=${OIFS}
else
    echo -e "ERROR: too many args
            usage: $0 IP1[,IP2[,...]] [ACTION]
            where
                IP1,IP2 is a comma separated IP list
                ACTION is to be chosen between restart, remove and reset (default: restart)"
    exit 1
fi

WGET_OPTIONS="--delete-after"

for IP in ${AASTRA_IP[@]}; do
    # First we log in
    wget ${WGET_OPTIONS} --http-user=${AASTRA_LOGIN} --http-password=${AASTRA_PASSWD} --read-timeout=5 --tries=1 http://${IP}/sysinfo.html
    # Then we do the appropriate action
    if [ ${AASTRA_ACTION} = "restart" ]; then
        wget ${WGET_OPTIONS} --http-user=${AASTRA_LOGIN} --http-password=${AASTRA_PASSWD} --post-data 'resetOption=0' --read-timeout=5 --tries=1 http://${IP}/reset.html
    elif [ ${AASTRA_ACTION} = "local" ]; then
        wget ${WGET_OPTIONS} --http-user=${AASTRA_LOGIN} --http-password=${AASTRA_PASSWD} --post-data 'resetOption=2' --read-timeout=5 --tries=1 http://${IP}/reset.html
    elif [ ${AASTRA_ACTION} = "factory" ]; then
        wget ${WGET_OPTIONS} --http-user=${AASTRA_LOGIN} --http-password=${AASTRA_PASSWD} --post-data 'resetOption=1' --read-timeout=5 --tries=1 http://${IP}/reset.html
    fi
done
