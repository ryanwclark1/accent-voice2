#!/bin/sh
# Usus dunamai to determine a semver compatible version for the current state of the project
# Useefull when building wheels in CI/CD on branches or merge requests, 
# without possibly overwriting released versions (of certain tag)
# Used to run in CI/CD, as it will modify both pyproject.toml's and python files (by setting the right string in `__version__=..`)
set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

# first run directly, to have script stop if dunamai isn't available (for example if not installed, or running in wrong virtual env)
dunamai from any
VERSION=$(dunamai from any)
echo $VERSION

# all python packages, in topological order
. ${DIR}/services.sh
_services=". ${SERVICES}"
echo "Running on following services: ${_services}"
if [ "$(uname)" = "Darwin" ]; then export SEP=" "; else SEP=""; fi
for p in $_services
do
  echo "Creating local version of ${p}"
  echo "$VERSION" > "${p}/VERSION"
  sed -i$SEP'' "s/^version = .*/version = \"$VERSION\"/" "$p/pyproject.toml"
done
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-agendtd/accent_agentd/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-amid/accent_amid/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-auth/accent_auth/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-call-logd/accent_call_logd/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-calld/accent_calld/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-confd/accent_confd/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-confgend/accent_confgend/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-dao/accent_dao/__init__.py
sed -i$SEP'' "s/^__version__.*/__version__ = \"$VERSION\"/" accent-manage-db/accent_manage_db/__init__.py