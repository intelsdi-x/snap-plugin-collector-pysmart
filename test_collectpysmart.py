#!/usr/bin/env python

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

import unittest
import commands
import pytest
from mock import Mock, patch
import snap_plugin.v1 as snap
from SmartmonCollectorPlugin import Smartmon

class SmartTestCase(unittest.TestCase):

    #tests if smartctl is installed, report and exit if it is not
    exist = commands.getstatusoutput("smartctl --scan")
    if "command not found" in exist[1]:
        pytest.xfail('smartctl not installed\n')

    # mock the DeviceList attribute in pySMART
    @patch('pySMART.DeviceList')
    def test_smartpy(self, mock_dev):
        mock_dev.devices = []
        #create device names and attributes to iterate through
        for deviter in ["/dev/sda", "/dev/sdb"]:
            mock_dev.devices.append(
                Mock(
                    name=deviter,
                    attributes=Mock(
                        name="asdf", thresh=5, value=7, raw=123, type='Old_age', updated='Always', worst='10', num='2', when_failed='-')))
        plugin = Smartmon("smart", 1)
        #set the two metrics for value and threshold
        metrics = plugin.collect([
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="value")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="threshold")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="raw")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="type")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="updated")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="worst")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="num")]),
            snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="smartmon"),
                    snap.NamespaceElement(value="devices"),
                    snap.NamespaceElement(name="device"),
                    snap.NamespaceElement(name="attribute"),
                    snap.NamespaceElement(value="when_failed")])
        ])
        # test that the metrics have been set in metrics
        assert len(metrics) > 0
