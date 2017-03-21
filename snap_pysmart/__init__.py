#!/usr/bin/env python

# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2017 Intel Corporation
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

import logging
import time
import sys

from pySMART import DeviceList

import snap_plugin.v1 as snap
from shutilwhich import which

LOG = logging.getLogger(__name__)


class Smartmon(snap.Collector):

    def __init__(self, *args, **kwargs):
        super(Smartmon, self).__init__(*args)
        if "DeviceList" in kwargs:
            self.devices = kwargs.get("DeviceList")().devices
        else:
            if which("smartctl") is None:
                sys.exit("smartctl needs to be installed")
            self.devices = []
            for device in DeviceList().devices:
                if not device.supports_smart:
                    LOG.warning("Skipping %s.  SMART is not enabled.", device.path)
                else:
                    self.devices.append(device)
            if len(self.devices) == 0:
                sys.exit("No devices detected.  Check permissions.  Hint run: 'smartctl --scan'")

    def update_catalog(self, config):
        LOG.debug("GetMetricTypes called")
        metrics = []
        # adds namespace elements (static and dynamic) via namespace methods
        for i in ("threshold", "value", "whenfailed", "worst", "type",
                  "updated", "raw", "num"):
            metric = snap.Metric(version=1,
                                 Description="SMARTMON list of dynamic devices"
                                 " and attributes")
            metric.namespace.add_static_element("intel")
            metric.namespace.add_static_element("smartmon")
            metric.namespace.add_static_element("devices")
            # dynamic elements which are captured from the smartmontool
            metric.namespace.add_dynamic_element("device", "device name")
            metric.namespace.add_dynamic_element("attribute", "attribute name")
            # values of the attributes to collect
            metric.namespace.add_static_element(i)
            metrics.append(metric)
        return metrics

    def get_config_policy(self):
        LOG.debug("GetConfigPolicy called")
        return snap.ConfigPolicy()

    def collect(self, metrics):
        metricsToReturn = []
        # set the time before the loop in case the time changes as the metric
        # values are being set
        ts_now = time.time()
        # loop through each device and each attribute on the device and store
        # the value to metric
        for dev in self.devices:
            # dev.attributes is the list of S.M.A.R.T. attributes avaible on
            # each device, may change depending on the devide
            for att in dev.attributes:
                if att is not None:
                    for metric in metrics:
                        # sets the metricTeReturn to the metrics class which
                        # inherits the namespace, unit, and tags from the
                        # metric in metrics
                        _metrics = snap.Metric(
                            namespace=[i for i in metric.namespace],
                            unit=metric.unit)
                        _metrics.tags = [(k, v) for k, v in metric.tags.items()]
                        # set the dynamic device name
                        _metrics.namespace[3].value = dev.name
                        # set the dynamic attribute name
                        _metrics.namespace[4].value = att.name
                        # store the value into the metric data
                        if _metrics.namespace[5].value == "threshold":
                            _metrics.data = att.thresh
                        if _metrics.namespace[5].value == "value":
                            _metrics.data = att.value
                        if _metrics.namespace[5].value == "whenfailed":
                            _metrics.data = att.when_failed
                        if _metrics.namespace[5].value == "worst":
                            _metrics.data = att.worst
                        if _metrics.namespace[5].value == "type":
                            _metrics.data = att.type
                        if _metrics.namespace[5].value == "updated":
                            _metrics.data = att.updated
                        if _metrics.namespace[5].value == "raw":
                            _metrics.data = att.raw
                        if _metrics.namespace[5].value == "num":
                            _metrics.data = att.num
                        # store the time stamp for each metric
                        _metrics.timestamp = ts_now
                        metricsToReturn.append(_metrics)
        return metricsToReturn

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
