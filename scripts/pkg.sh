#!/bin/bash

#http://www.apache.org/licenses/LICENSE-2.0.txt
#
#
#Copyright 2016 Intel Corporation
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

set -e
set -u
set -o pipefail

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__proj_dir="$(dirname "$__dir")"
__acbuild_ver="v0.4.0"

. "${__dir}/common.sh"

PLUGIN_DIR=$1
PLUGIN_NAME=$2

if [[ -d "${__proj_dir}/dist" ]]; then
    _warning "dist already exists.  Hint: run make clean"
    exit 0
fi
mkdir -p "${__proj_dir}/dist"

_debug "verifying we are running on a Linux system"
if [[ $OSTYPE != "linux-gnu" ]]
then
    _error "This script can only be run from a Linux system"
    exit 1
fi

if ! type acbuild 2> /dev/null; then
    _info "Downloading acbuild tool..."
    set +e
    $(cd ${__proj_dir}/dist && mkdir acbuild-${__acbuild_ver} && wget -L -O- https://github.com/containers/build/releases/download/${__acbuild_ver}/acbuild-${__acbuild_ver}.tar.gz | tar zxv)
    set -e
    PATH="$PATH:${__proj_dir}/dist/acbuild-${__acbuild_ver}"
fi

if ! type pyenv 2> /dev/null; then
    echo "please install pyenv"
    _info "hint: see https://github.com/yyuu/pyenv"
    exit 1
fi

# Prepare Python 2.7 virtual environment
# NOTE: PYTHON_ENV is not the same as VIRTUAL_ENV, second one points to environment
# created by Travis CI, that we're in - each Python version in .travis.yml
# is created by Travis CI as separate virtual env.
# See: https://docs.travis-ci.com/user/languages/python/#Travis-CI-Uses-Isolated-virtualenvs
pyenv install -s 2.7.12
PYTHON_ENV=$(pyenv prefix 2.7.12)
_info "preparing virtual environment $PYTHON_ENV"
_info "virtual environment: installing plugin requirements"
$PYTHON_ENV/bin/pip install -r ${__proj_dir}/requirements.txt
_info "virtual environment: installing plugin package"
$PYTHON_ENV/bin/pip install -I ${__proj_dir}
_info "virtual environment: making relocatable"

_info "packaging ${__proj_dir}/${PLUGIN_DIR}"
acbuild begin
_info "packaging: setting name ${PLUGIN_NAME}"
acbuild set-name ${PLUGIN_NAME}
_info "packaging: copying python virtual environment"
acbuild copy $PYTHON_ENV .venv
_info "packaging: setting plugin startup command"
acbuild set-exec ./.venv/bin/${PLUGIN_NAME}
_info "packaging: writing ${__proj_dir}/dist/${PLUGIN_NAME}/linux/${HOSTTYPE}/${PLUGIN_NAME}-linux-${HOSTTYPE}.aci"
mkdir -p "${__proj_dir}/dist/${PLUGIN_NAME}/linux/${HOSTTYPE}"
acbuild write ${__proj_dir}/dist/${PLUGIN_NAME}/linux/${HOSTTYPE}/${PLUGIN_NAME}-linux-${HOSTTYPE}.aci
acbuild end
_info "removing: ${__proj_dir}/acbuild-${__acbuild_ver}"
rm -rf ${__proj_dir}/dist/acbuild-${__acbuild_ver}
_info "ACI package build finished"

