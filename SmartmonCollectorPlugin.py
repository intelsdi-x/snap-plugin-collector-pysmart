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
import pySMART #required for gathering S.M.A.R.T. metrics

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)

class Smartmon(snap.Collector):    

    def update_catalog(self, config):
        LOG.debug("GetMetricTypes called")
        metrics = []        
        # adds namespace elements (static and dynamic) via namespace methods
        for i in ("threshold", "value"):
            metric = snap.Metric(version=1, Description="SMARTMON list of dynamic devices and attributes")
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
        from pySMART import DeviceList
        metricsToReturn = []
        # dev will be a list of devices on the system for which S.M.A.R.T. is enabled
        devList=DeviceList()
        # set the time before the loop in case the time changes as the metric values are being set
        ts = time.time()
        #l oop through each device and each attribute on the device and store the value to metric
        for dev in devList.devices:
            # dev.attributes is the list of S.M.A.R.T. attributes avaible on each device, 
            # may change depending on the devide
            for att in dev.attributes:
                if att!=None:
                    for metric in metrics:   
                        # sets the metricTeReturn to the metrics class which inherits the namespace, unit, and tags from the metric in metrics 
                        metricToReturn=snap.Metric(namespace=[i for i in metric.namespace], unit=metric.unit)   
                        metricToReturn.tags=[(k,v) for k,v in metric.tags.items()] 
                        # set the dynamic device name         
                        metricToReturn.namespace[3].value = dev.name
                        # set the dynamic attribute name
                        metricToReturn.namespace[4].value = att.name
                        # store the value into the metric data
                        if metricToReturn.namespace[5].value == "threshold":                         
                            metricToReturn.data = att.thresh
                        if metricToReturn.namespace[5].value == "value":                             
                            metricToReturn.data = att.value
                        # store the time stamp for each metric
                        metricToReturn.timestamp=ts
                        metricsToReturn.append(metricToReturn)
        return metricsToReturn

if __name__ == "__main__":
    Smartmon("SmartmonCollectorPlugin-py", 1).start_plugin()
    