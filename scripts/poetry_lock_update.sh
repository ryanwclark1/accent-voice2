#!/bin/sh
# This script reflects the latest changes of pyproject.toml
#  into both the poetry.lock file and the virtualenv.
#  by running `poetry update && poetry install --sync`
# It first configures poetry to use the right python for creation of the virtual env
set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

# all python libraries, in topological order
. ${DIR}/libraries.sh
_libraries=". ${LIBRARIES}"
echo "Running on following services: ${_libraries}"
for p in $_libraries
do
  cd "${DIR}/../library/${p}" || exit
  (pyenv local && poetry env use $(which python)) || poetry env use 3.12
  poetry update && poetry install --sync
done


# # all python packages, in topological order
. ${DIR}/services.sh
_services=". ${SERVICES}"
echo "Running on following services: ${_services}"
for p in $_services
do
  cd "${DIR}/../service/${p}" || exit
  (pyenv local && poetry env use $(which python)) || poetry env use 3.12
  poetry update && poetry install --sync
done

