#!/usr/bin/env bash
# This script reflects the latest changes of pyproject.toml
#  into both the poetry.lock file and the virtualenv.
#  by running `poetry lock --no-update && poetry install --sync`
# It first configures poetry to use the right python for creation of the virtual env
set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

. ${DIR}/services.sh
_services=". ${SERVICES}"
echo "Running on following services: ${_services}"
for p in $_services
do
  cd "${DIR}/services/${p}" || exit
  echo "Building ${p}"
  echo "Dir is ${DIR}"
  pwd
  # docker build -f "Dockerfile" -t "${p}":latest "$build_context"
  # docker tag "${p}":latest accentcommunications/"${p}":latest
  # docker push accentcommunications/"${p}":latest
done
