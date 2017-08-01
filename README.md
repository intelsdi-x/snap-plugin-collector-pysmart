# Snap collector plugin - Smartmon in python
This Snap plugin collects metrics from the Self-Monitoring, Analysis and Reporting Technology (S.M.A.R.T.) leveraging the pySMART library. The purpose of S.M.A.R.T. is to monitor the reliability of the hard drive and predict drive failures, and to carry out different types of drive self-tests.

It's used in the [Snap framework](http://github.com/intelsdi-x/snap).

1. [Getting Started](#getting-started)
  * [System Requirements](#system-requirements)
  * [Installation](#installation)
  * [Configuration and Usage](#configuration-and-usage)
2. [Documentation](#documentation)
  * [Collected Metrics](#collected-metrics)
  * [Examples](#examples)
  * [Roadmap](#roadmap)
3. [Community Support](#community-support)
4. [Contributing](#contributing)
5. [License](#license)
6. [Acknowledgements](#acknowledgements)

## Getting Started
### System Requirements 
* [python 2.7+](https://www.python.org/downloads/)
* [smartmontools](https://www.smartmontools.org)
* [pyenv 1.0.10+](https://github.com/pyenv/pyenv)
* [acbuild 0.4.0+](https://github.com/containers/build)
    The acbuild tool will be downloaded automatically while building ACI package, but it is recommended to install it manually in your system to speed up build process. For Ubuntu, you can do it just by:

    ```
    sudo apt-get install acbuild
    ```

For testing:
* [tox](https://tox.readthedocs.io/en/latest/) (install using `pip install tox`)

### Operating systems
All OSs currently supported by snap:
* Linux/amd64
* Darwin/amd64

### Installation
#### Download pysmart plugin binary:
You can get the pre-built binaries for your OS and architecture under the plugin's [release](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/releases) page.  For Snap, check [here](https://github.com/intelsdi-x/snap/releases).


#### To build the plugin binary:
Fork https://github.com/intelsdi-x/snap-plugin-collector-pysmart

Clone repo into `$GOPATH/src/github.com/intelsdi-x/`:

```
$ git clone https://github.com/<yourGithubID>/snap-plugin-collector-pysmart.git
```

Run `make pkg` to build package. Package will be available under "dist" folder.

NOTE: If you got Snap error "received metric with bad version" during development (after adding some commits), run "git tag -af <YOUR_VERSION> -m <VERSION_INFO>" or just "git tag -f <YOUR_VERSION>" to update version tag, and rebuild package. Plugin version is gathered from git tags.

### Configuration and Usage
* Set up the [Snap framework](https://github.com/intelsdi-x/snap/blob/master/README.md#getting-started)
* [Snap Python documentation](https://intelsdi-x.github.io/snap-plugin-lib-py/index.html)

## Documentation

There are a number of other resources you can review to learn to use this plugin:
* [Snap pysmart examples](#examples)

### Collected Metrics
This plugin will identify all the devices on the node which have [S.M.A.R.T.](https://www.smartmontools.org/) enabled and automatically populate the list of collected metrics based on which are being exposed by the device. This will be different per manufacturer and per device. 

* Ensure that S.M.A.R.T. is enabled on the device

Below is an example of the metrics being gathered by the Intel 3700 SSD
* Note: $deviceName will be dependent on the path (i.e. /dev/sda1)

Namespace | Description (optional)
----------|-----------------------
/intel/smartmon/devices/$deviceName/Reserve_Block_Count | available reserved space raw value 
/intel/smartmon/devices/$deviceName/Program_Fail_Count | shows total count of program fails
/intel/smartmon/devices/$deviceName/Unexpected_Power_Loss_Count | reports number of unclean shutdowns, cumulative over the life of the ssd
/intel/smartmon/devices/$deviceName/Power_Loss_Cap_Test | last test result as microseconds to discharge cap
/intel/smartmon/devices/$deviceName/SATA_Downshift_Count | reports number of times SATA interface selected lower signaling rate due to error
/intel/smartmon/devices/$deviceName/Temperature_Case | reports SSD case temperature statistics
/intel/smartmon/devices/$deviceName/Unsafe_Shutdown_Count | reports the cumulative number of unsafe (unclean) shutdown events over the life of the device
/intel/smartmon/devices/$deviceName/Temperature_Internal | reports internal temperature of the SSD in degrees Celsius
/intel/smartmon/devices/$deviceName/CRC_Error_Count | shows total number of encountered SATA interface cyclic redundancy check (CRC) errors
/intel/smartmon/devices/$deviceName/Host_Writes_32mb | reports total number of sectors written by the host system
/intel/smartmon/devices/$deviceName/Timed_Workload_Host_ReadWrite_Ratio | shows the percentage of I/O operations that are read operations 
/intel/smartmon/devices/$deviceName/Timed_Workload_Timer | measures the elapsed time, number of minutes since starting this workload timer 
/intel/smartmon/devices/$deviceName/Thermal_Throttle | reports Percent Throttle Status and Count of events 
/intel/smartmon/devices/$deviceName/Host_Writes_32mb_Total_LBAs_Written | reports the total number of sectors written by the host system
/intel/smartmon/devices/$deviceName/Host_Reads_32mb_Total_LBAs_Read | reports the total number of sectors read by the host system
/intel/smartmon/devices/$deviceName/NAND_Writes_32mb | reports the total number of sectors writen by the host system


### Examples
This is an example running pysmart and writing data to a file. It is assumed that you are using the latest Snap binary and plugins.

The example is run from a directory which includes snaptel, snapteld, along with the plugins and task file.

Before starting the Snap daemon, install smartmontools using:
```
$ brew install smartmontools
```
Run the smartctl command using:
```
$ smartctl --scan
IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice -d ata # IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice, ATA device
```
Enable SMART, for example:
```
smartctl -s on IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice
```

#### Preparing environment
If you want to edit plugin code, it is not needed to build ACI package every time the source code changed.
It is quite easy to prepare virtual environment, so you don't need to install requirements and specific Python version directly on your machine:

1. Install Python 2.7.12 as your virtual environment and switch to it globally:
    ```
    pyenv install -s 2.7.12
    pyenv global 2.7.12
    ```
2. Install requirements in your virtual environment:
    ```
    pip install -r requirements.txt
    pip install -r test-requirements.txt
    ```

After completing these steps, you can just start Python scripts and tools like `pip` as usual, but Python 2.7.12 will be used by default. You can find all environment files and installed packages in `$HOME/.pyenv/versions/2.7.12`. If you want to switch back to your system default Python version, type `pyenv global system`.

#### Loading plugin

##### Load directly from source:

Start the Snap daemon with root permissions (needed by pySMART library). As sudo resets all environment variables by default, you will need to pass PATH / PYTHONPATH environment variables for Snap to be able to access your Python virtual environment and plugin modules.

In plugin root directory run:
```
$ sudo PATH=$PATH PYTHONPATH=$(pwd) snapteld -l 1 -t 0
```
*The option "-l 1" is for setting the debugging log level and "-t 0" is for disabling plugin signing.*

Then you can simply load plugin directly from source:
```
$ snaptel plugin load snap_pysmart/plugin.py
Plugin loaded
Name: smartmoncollectorplugin-py
Version: 1
Type: collector
Signed: false
Loaded Time: Thu, 20 Jul 2017 16:57:35 CEST
```

##### Load from ACI package:

If using ACI package, you don't need to pass any environment variables, just start Snap daemon with root permissions:
```
$ sudo snapteld -l 1 -t 0
```

Then load pysmart plugin from ACI package:
```
$ snaptel plugin load dist/snap-plugin-collector-pysmart/linux/x86_64/snap-plugin-collector-pysmart-linux-x86_64.aci
Plugin loaded
Name: smartmoncollectorplugin-py
Version: 1
Type: collector
Signed: false
Loaded Time: Tue, 21 Mar 2017 11:20:05 PDT
```

##### Plugin diagnostics
Plugin diagnostics allows to preview plugin info such as metric catalog or collected metrics without loading plugin in Snap. It is really helpful when testing changes in plugin source code.

To start plugin diagnostics, in plugin root directory run:
```
$ sudo PATH=$PATH PYTHONPATH=$(pwd) snap_pysmart/plugin.py
```

#### Creating task for plugin
See available metrics for your system. *Note* The * in the metric list name indicates a dynamic metric which will update depending on the device names and attribute names
```
$ snaptel metric list
```

Get file plugin for publishing and load it:
```
$ wget  http://snap.ci.snap-telemetry.io/plugins/snap-plugin-publisher-file/latest/linux/x86_64/snap-plugin-publisher-file
$ chmod 755 snap-plugin-publisher-file

$ snaptel plugin load snap-plugin-publisher-file
```

Create a task file. For example, task-smart.json:

Creating a task manifest file. 
```
{
    "version": 1,
    "schedule": {
        "type": "simple",
        "interval": "1s"
    },
    "workflow": {
        "collect": {
            "metrics": {
                "/intel/smartmon/devices/*/*/threshold": {},
                "/intel/smartmon/devices/*/*/value": {},
                "/intel/smartmon/devices/*/*/whenfailed": {},
                "/intel/smartmon/devices/*/*/worst": {},
                "/intel/smartmon/devices/*/*/type": {},
                "/intel/smartmon/devices/*/*/updated": {},
                "/intel/smartmon/devices/*/*/raw": {},
                "/intel/smartmon/devices/*/*/num": {}
            },
            "publish": [
                {
                    "plugin_name": "file",
                    "config": {
                        "file": "/tmp/published_pysmart"
                    }
                }
            ]
        }
    }
}
```


See [exemplary task manifest](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/blob/master/examples/tasks/task-smart.json) 

Start task:
```
$ snaptel task create -t task-smart.json
Using task manifest to create task
Task created
ID: c6d095a6-733d-40cf-a986-9c82aa64b4e2
Name: Task-c6d095a6-733d-40cf-a986-9c82aa64b4e2
State: Running
```

See the pysmart plugin task
```
$ snaptel task list
ID 					 NAME 						 STATE 		 HIT 	 MISS 	 FAIL 	 CREATED 		 LAST FAILURE
c6d095a6-733d-40cf-a986-9c82aa64b4e2 	 Task-c6d095a6-733d-40cf-a986-9c82aa64b4e2 	 Running 	 9 	 0 	 0 	 10:39AM 2-23-2017
```
Watch the collection of the metrics
```
$ snaptel task watch c6d095a6-733d-40cf-a986-9c82aa64b4e2
```

See std output stream as the metrics are collected
```
|intel|smartmon|devices|IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice|Power-Off_Retract_Count|threshold 	 000 	 2017-02-23 10:45:44.698632001 -0800 PST
|intel|smartmon|devices|IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice|Power-Off_Retract_Count|value 	 099 	 2017-02-23 10:45:44.698632001 -0800 PST
|intel|smartmon|devices|IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice|Power_Cycle_Count|threshold 		 000 	 2017-02-23 10:45:44.698632001 -0800 PST
|intel|smartmon|devices|IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice|Power_Cycle_Count|value 		 094 	 2017-02-23 10:45:44.698632001 -0800 PST
|intel|smartmon|devices|IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice|Power_On_Hours|threshold 		 000 	 2017-02-23 10:45:44.698632001 -0800 PST
|intel|smartmon|devices|IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice|Power_On_Hours|value 			 099 	 2017-02-23 10:45:44.698632001 -0800 PST
```

Stop task:
```
$ snaptel task stop c6d095a6-733d-40cf-a986-9c82aa64b4e2
Task stopped:
ID: c6d095a6-733d-40cf-a986-9c82aa64b4e2
```

An example of how to deploy the pysmart plugin:
![img](https://cloud.githubusercontent.com/assets/3925702/24318732/2e5124a0-10c7-11e7-8628-7ce0221ec81e.gif)


### Roadmap
There isn't a current roadmap for this plugin, but it is in active development. As we launch this plugin, we do not have any outstanding requirements for the next release. If you have a feature request, please add it as an [issue](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/issues/new) and/or submit a [pull request](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/pulls).

## Community Support
This repository is one of **many** plugins in **Snap**, a powerful telemetry framework. See the full project at http://github.com/intelsdi-x/snap To reach out to other users, head to the [main framework](https://github.com/intelsdi-x/snap#community-support)

## Contributing
We love contributions!

There's more than one way to give back, from examples to blogs to code updates. See our recommended process in [CONTRIBUTING.md](CONTRIBUTING.md).

## License
[Snap](http://github.com/intelsdi-x/snap), along with this plugin, is an Open Source software released under the Apache 2.0 [License](LICENSE).

## Acknowledgements
* Authors: [Samantha Alt](https://github.com/saalt),
           [Joel Cooklin](https://github.com/jcooklin)

And **thank you!** Your contribution, through code and participation, is incredibly important to us.
