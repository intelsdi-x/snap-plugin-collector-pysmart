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

. "${__dir}/common.sh"

acbuild_ver="v0.4.0"
_version=`echo $(git describe 2>/dev/null || $(git symbolic-ref --short -q HEAD)-$(git rev-parse --short HEAD 2> /dev/null))`
_git_commit=`git rev-parse HEAD`
VERSION=${VERSION:-${_version}}

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

_info "Downloading acbuild tool"
set +e
$(cd ${__proj_dir}/dist && mkdir acbuild-${acbuild_ver} && wget -L -O- https://github.com/containers/build/releases/download/${acbuild_ver}/acbuild-${acbuild_ver}.tar.gz | tar zxv)
set -e
PATH="$PATH:${__proj_dir}/dist/acbuild-${acbuild_ver}"

if ! type pyenv >> /dev/null; then
    echo "install pyenv"
    _info "hint: see https://github.com/yyuu/pyenv"
    exit 1
fi

pyenv install -s 2.7.12

_debug "running: pip install -r requirements.txt"
$(pyenv prefix 2.7.12)/bin/pip install -r ${__proj_dir}/requirements.txt
_info "installing snap-plugin-collector-pysmart"
$(pyenv prefix 2.7.12)/bin/pip install ${__proj_dir}

_info "packaging ${__proj_dir}/SmartmonCollectorPlugin.py"
_info "running: acbuild begin"
acbuild begin
_info "running: acbuild set-name snap-plugin-collector-pysmart"
acbuild set-name snap-plugin-collector-pysmart
_info "running: rsync $VIRTUAL_ENV .venv-relocatable -a --copy-links -v"
rsync $(pyenv prefix 2.7.12)/ .venv-relocatable -q --delete -a --copy-links -v
_info "running: acbuild copy $VIRTUAL_ENV .venv-relocatable"
acbuild copy .venv-relocatable .venv
_info "running: acbuild copy ${__proj_dir}/snap_pysmart/plugin.py plugin.py"
acbuild copy ${__proj_dir}/snap_pysmart/plugin.py plugin.py
_info "creating run.sh"
cat <<EOF>run.sh
#!/bin/bash

DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}"  )" && pwd  )"
LD_LIBRARY_PATH=\${DIR}/.venv/lib
\${DIR}/.venv/bin/python plugin.py
EOF
chmod 755 run.sh
_info "running: acbuild copy run.sh run.sh"
acbuild copy run.sh run.sh
_info "running: acbuild set-exec run.sh"
acbuild set-exec run.sh
_info "running: acbuild set-exec ./.venv/bin/python plugin"
acbuild set-exec ./.venv/bin/python plugin.py
_info "running: write ${__proj_dir}/dist/snap-plugin-collector-pysmart/${VERSION}/linux/${HOSTTYPE}/snap-plugin-collector-pysmart-${VERSION}-linux-x86_64.aci"
mkdir -p "${__proj_dir}/dist/snap-plugin-collector-pysmart/${VERSION}/linux/${HOSTTYPE}"
acbuild write ${__proj_dir}/dist/snap-plugin-collector-pysmart/${VERSION}/linux/${HOSTTYPE}/snap-plugin-collector-pysmart-${VERSION}-linux-x86_64.aci
_info "running acbuild write ${__proj_dir}/dist/snap-plugin-collector-pysmart/latest/linux/${HOSTTYPE}/snap-plugin-collector-pysmart-linux-x86_64.aci"
mkdir -p "${__proj_dir}/dist/snap-plugin-collector-pysmart/latest/linux/${HOSTTYPE}"
acbuild write ${__proj_dir}/dist/snap-plugin-collector-pysmart/latest/linux/${HOSTTYPE}/snap-plugin-collector-pysmart-linux-x86_64.aci
_info "running: acbuild end"
acbuild end

_info "running: rm -rf ${__proj_dir}/acbuild-${acbuild_ver}"
rm -rf ${__proj_dir}/dist/acbuild-${acbuild_ver}

_info "done"