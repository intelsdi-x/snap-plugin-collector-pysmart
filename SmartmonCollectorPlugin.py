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
 
import logging
import time
from pySMART import DeviceList

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)


class Smartmon(snap.Collector):

    def update_catalog(self, config):
        LOG.debug("GetMetricTypes called")
        metrics = []
        # adds namespace elements (static and dynamic) via namespace methods
        for i in ("threshold", "value"):
            metric = snap.Metric(version=1, Description="SMARTMON list of "
                                 + "dynamic devices and attributes")
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
        # devices on the system for which S.M.A.R.T. is enabled
        devices = DeviceList()
        # set the time before the loop in case the time changes as the metric
        # values are being set
        ts_now = time.time()
        # loop through each device and each attribute on the device and store
        # the value to metric
        for dev in devices.devices:
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
                        # store the time stamp for each metric
                        _metrics.timestamp = ts_now
                        metricsToReturn.append(_metrics)
        return metricsToReturn

if __name__ == "__main__":
    Smartmon("SmartmonCollectorPlugin-py", 1).start_plugin()
