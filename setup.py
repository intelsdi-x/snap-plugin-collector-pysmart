# -*- coding: utf-8 -*-
# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
import versioneer


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="snap-plugin-collector-pysmart",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=['snap-plugin-lib-py>=1.0.10,<2','pySMART.smartx>=0.3.6',
                      'shutilwhich>=1.1.0'],
    author="Joel Cooklin",
    author_email="joel.cooklin@gmail.com",
    description="This is a plugin for the Snap telemetry framework providing" +
                "storage related metrics through smartmontools",
    entry_points={
        'console_scripts': [
            'snap-plugin-collector-pysmart=snap_pysmart.plugin:run'
        ]
    },
    long_description=readme(),
    license="Apache 2.0",
    keywords="snap telemetry plugin plugins metrics smartmon smartmontools",
    url="http://github.com/intelsdi-x/snap-plugin-collector-pysmart"
)
