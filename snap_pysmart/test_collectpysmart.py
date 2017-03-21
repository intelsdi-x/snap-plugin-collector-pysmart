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

import pytest
from mock import MagicMock, Mock

import snap_plugin.v1 as snap
from shutilwhich import which
from . import Smartmon


class SmartTestCase(unittest.TestCase):

    # mock the DeviceList attribute in
    def test_smartpy(self):

        # setup mocks
        att = Mock()
        att.name = "some-attribute"
        att.value = 5
        att.thresh = 5
        att.raw = 123
        att.type = "old_age"
        att.updated = "always"
        att.worst = "2"
        att.num = "7"
        att.when_failed = "-"
        device = MagicMock()
        device.name = "/dev/sda"
        device.attributes.__iter__.return_value = [att]
        mock_devices = MagicMock()
        mock_devices.devices.__iter__.return_value = iter([device])
        mock_devlist = Mock()
        mock_devlist.return_value = mock_devices

        assert not mock_devlist.called
        plugin = Smartmon("smart", 1, DeviceList=mock_devlist)
        assert mock_devlist.called
        # set the two metrics for value and threshold
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
