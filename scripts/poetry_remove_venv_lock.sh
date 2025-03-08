#!/usr/bin/env bash
# This script removes the poetry.lock file and the virtualenv.
set -x
set -u
set -e

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

# Source the services and libraries files
. ${DIR}/services.sh
. ${DIR}/libraries.sh

# Process services
echo "Running on following services:"
echo "$SERVICES"
for p in $SERVICES
do
    # Skip empty lines
    [ -z "$p" ] && continue

    echo "Processing service: $p"
    cd "${DIR}/../service/${p}" || exit
    rm -rf .venv
    rm -rf poetry.lock
done

# Process libraries
echo "Running on following libraries:"
echo "$LIBRARIES"
for p in $LIBRARIES
do
    # Skip empty lines
    [ -z "$p" ] && continue

    echo "Processing library: $p"
    cd "${DIR}/../library/${p}" || exit
    rm -rf .venv
    rm -rf poetry.lock
done

echo "Cleanup complete"