#!/bin/sh
# This script builds all the poetry packages, creating wheels, dists, and requirements.txt's
# All the wheels will be placed in both the root folder's dist, and in a dist folder within each package
set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

poetry version
VERSION=$(poetry version | awk '{print $2}')

if [ "$(uname)" = "Darwin" ]; then export SEP=" "; else SEP=""; fi

# all python packages, in topological order
. ${DIR}/services.sh
_services=$SERVICES
echo "Running on following services: ${_services}"
for p in $_services
do
  cd "${DIR}/../${p}" || exit
  # change path deps in service def
  sed -i$SEP'' "s|{.*path.*|\"^$VERSION\"|" pyproject.toml
  # include project changelog
  cp ../CHANGELOG.md ./
  poetry build
  # export deps, with updated path deps
  mkdir -p info
  poetry export -f requirements.txt --output ./info/requirements.txt --without-hashes --with-credentials
  sed -i$SEP'' "s/ @ .*;/==$VERSION;/" "./info/requirements.txt"
  ls -altr ./dist/
done

# -u for update
if [ "$(uname)" = "Darwin" ]; then export FLAG=" "; else FLAG="-u "; fi
echo "=========="
mkdir -p "${DIR}/../info"
cp $FLAG "${DIR}/../CHANGELOG.md" "${DIR}/../info/"
cp $FLAG "${DIR}/../VERSION" "${DIR}/../info/"
echo "=========="
# copying each wheel to root folder dist
mkdir -p "${DIR}/../dist"
for p in $_services
do
  ls -altr "${DIR}/../${p}/dist/"
  cp $FLAG "${DIR}/../${p}/dist/"*".whl" "${DIR}/../dist/"
done
echo "=========="
ls -altr "${DIR}/../dist/"
# then copying these to each service
for p in $_services
do
  cp $FLAG "${DIR}/../dist/"*".whl" "${DIR}/../${p}/dist/"
  cp $FLAG "${DIR}/../info/"*"" "${DIR}/../${p}/info/"
  ls -altr "${DIR}/../${p}/dist/"
done
