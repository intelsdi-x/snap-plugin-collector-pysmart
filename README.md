
# DISCONTINUATION OF PROJECT 

**This project will no longer be maintained by Intel.  Intel will not provide or guarantee development of or support for this project, including but not limited to, maintenance, bug fixes, new releases or updates.  Patches to this project are no longer accepted by Intel. If you have an ongoing need to use this project, are interested in independently developing it, or would like to maintain patches for the community, please create your own fork of the project.**


# Snap collector plugin - Smartmon in python
This Snap plugin collects metrics from the Self-Monitoring, Analysis and Reporting Technology (S.M.A.R.T.) leveraging the pySMART library. The purpose of S.M.A.R.T. is to monitor the reliability of the hard drive and predict drive failures, and to carry out different types of drive self-tests.

It's used in the [Snap framework](http://github.com/intelsdi-x/snap).

1. [Getting Started](#getting-started)
  * [System Requirements](#system-requirements)
  * [Operating systems](#operating-systems)
  * [Installation](#installation)
  * [Configuration and Usage](#configuration-and-usage)
2. [Documentation](#documentation)
  * [Collected Metrics](#collected-metrics)
  * [Examples](#examples)
  * [Roadmap](#roadmap)
3. [Community Support](#community-support)
4. [Contributing](#contributing)
5. [License](#license)

## Getting Started
### System Requirements 
* [smartmontools](https://www.smartmontools.org)
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
The plugin should work on any platform with Python2.7 and where smartclt is installed.  The plugin has been tested on Linux and MacOS.

### Installation
#### Python module

The preferred way to run Python based plugins is to leverage the python package
index.  This means that the Snap daemon, *snapteld*, will need to be run in an
environment where the python module `snap-plugin-collector-pysmart` was installed.
If you install the plugin (`pip install snap-plugin-collector-pysmart`) into the
system's Python environment that should be enough.  If you use a
[virtualenv](https://pypi.python.org/pypi/virtualenv) be sure to activate it 
before starting `snapteld` since it will need access to the plugin and its
dependencies.

To install the plugin run: 
* `pip install snap-plugin-collector-pysmart`

The plugin includes a command line entry point also called
`snap-plugin-collector-pysmart` which should be in your path after installation.

Find the plugin's command line script:
* `which snap-plugin-collector-pysmart`

```
which snap-plugin-collector-pysmart
> /Users/jrcookli/.pyenv/versions/py2712/bin/snap-plugin-collector-pysmart
```

The entry point script, snap-plugin-collector-pysmart, is what we will be
load into `snapteld` with the following command.

```
snaptel plugin load `which snap-plugin-collector-pysmart`
```

#### Plugin package

An alternative installation method for Linux X86_64 is to use the binary package.
The package includes a Python 2.7 distribution with the plugin already installed.

You can get the pre-built plugin package under
[releases](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/releases)
page.

Known issues:
* Longer plugin load times 
* A package is only available for Linux X86_64

Since the current default timeout may be exceeded start `snapteld` with the flag
`--plugin-load-timeout 30` (e.g. `snapteld -t 0 -1 --plugin-load-timeout 30`).
Lastly, when you load the plugin you will also want to increase the clients
timeout using the flag `--timeout 30s` (e.g. `snaptel --timeout 30s plugin load snap-plugin-collector-pysmart`).

### Configuration and Usage
* Start snapteld
  * See the Snap [readme](https://github.com/intelsdi-x/snap/blob/master/README.md#getting-started) for getting started details
  * Start snap: `snapteld -t 0 -l 1`
* Ensure that smartctl is **installed** and **enabled**
  * To install smartctl run:
     * On MacOS `brew install smartmontools`
     * On Ubuntu `apt-get install smartmontools`
     * On RedHat/CentOS `yum install smartmontools`
  * To ensure SMART is enabled run:
    * `smartctl --scan`

## Documentation
### Collected Metrics
This plugin will identify all the devices on the node which have [S.M.A.R.T.](https://www.smartmontools.org/) enabled and automatically populate the list of collected metrics based on which are being exposed by the device. This will be different per manufacturer and per device.

Below is an example of the metrics being gathered by the Intel 3700 SSD
* Note: $deviceName will be dependent on the path (i.e. /dev/sda1)

Namespace | Data Type | Description (optional)
----------|-----------|-----------------------
/intel/smartmon/devices/$deviceName/Reserve_Block_Count | string | available reserved space raw value
/intel/smartmon/devices/$deviceName/Program_Fail_Count | string | shows total count of program fails
/intel/smartmon/devices/$deviceName/Unexpected_Power_Loss_Count | string | reports number of unclean shutdowns, cumulative over the life of the ssd
/intel/smartmon/devices/$deviceName/Power_Loss_Cap_Test | string | last test result as microseconds to discharge cap
/intel/smartmon/devices/$deviceName/SATA_Downshift_Count | string | reports number of times SATA interface selected lower signaling rate due to error
/intel/smartmon/devices/$deviceName/Temperature_Case | string | reports SSD case temperature statistics
/intel/smartmon/devices/$deviceName/Unsafe_Shutdown_Count | string | reports the cumulative number of unsafe (unclean) shutdown events over the life of the device
/intel/smartmon/devices/$deviceName/Temperature_Internal | string | reports internal temperature of the SSD in degrees Celsius
/intel/smartmon/devices/$deviceName/CRC_Error_Count | string | shows total number of encountered SATA interface cyclic redundancy check (CRC) errors
/intel/smartmon/devices/$deviceName/Host_Writes_32mb | string | reports total number of sectors written by the host system
/intel/smartmon/devices/$deviceName/Timed_Workload_Host_ReadWrite_Ratio | string | shows the percentage of I/O operations that are read operations
/intel/smartmon/devices/$deviceName/Timed_Workload_Timer | string | measures the elapsed time, number of minutes since starting this workload timer
/intel/smartmon/devices/$deviceName/Thermal_Throttle | string | reports Percent Throttle Status and Count of events
/intel/smartmon/devices/$deviceName/Host_Writes_32mb_Total_LBAs_Written | string | reports the total number of sectors written by the host system
/intel/smartmon/devices/$deviceName/Host_Reads_32mb_Total_LBAs_Read | string | reports the total number of sectors read by the host system
/intel/smartmon/devices/$deviceName/NAND_Writes_32mb | string | reports the total number of sectors writen by the host system

### Examples
In this example we will collect data from SMART and publish it to a file. It is assumed that you are using the latest Snap binary and plugins.

The example is run from a directory which includes snaptel, snapteld, along with the plugins and task file.

1. Verify S.M.A.R.T is enable

  * Run the smartctl command using:
```
$ smartctl --scan
IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice -d ata # IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice, ATA device
```
  * Enable SMART:
```
smartctl -s on IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/RP06@1C,5/IOPP/SSD0@0/AppleAHCI/PRT0@0/IOAHCIDevice@0/AppleAHCIDiskDriver/IOAHCIBlockStorageDevice
```

2. Start the Snap daemon:

  * Run:

  ```
  $ snapteld -l 1 -t 0
  ```

  The option "-l 1" is for setting the debugging log level and "-t 0" is for disabling plugin signing.

3.  Load the plugin:

  * Run (in a different terminal):

```
$ snaptel plugin load `which snap-plugin-collector-pysmart`
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

  * List the metric catalog by running:

```
$ snaptel metric list
NAMESPACE 				 VERSIONS
/intel/smartmon/devices/*/*/num 	 1
/intel/smartmon/devices/*/*/raw 	 1
/intel/smartmon/devices/*/*/threshold 	 1
/intel/smartmon/devices/*/*/type 	 1
/intel/smartmon/devices/*/*/updated 	 1
/intel/smartmon/devices/*/*/value 	 1
/intel/smartmon/devices/*/*/whenfailed 	 1
/intel/smartmon/devices/*/*/worst 	 1
```

  See available metrics for your system. Note the `*` in the metric list.  It
  indicates a dynamic metric which will be update depending on the device names
  and attribute available on the system being monitored.

4.  Download the file publisher plugin and load it

  *  Get the latest file publisher plugin by running:

```
$ wget  http://snap.ci.snap-telemetry.io/plugins/snap-plugin-publisher-file/latest/linux/x86_64/snap-plugin-publisher-file
```

  * Load the file publisher plugin by running:

```
$ snaptel plugin load snap-plugin-publisher-file
Plugin loaded
Name: file
Version: 2
Type: publisher
Signed: false
Loaded Time: Sat, 22 Apr 2017 14:47:59 PDT
```

  * Create a task file by running:

```
cat <<EOF>pysmart-file.yaml
---
  version: 1
  schedule:
    type: "simple"
    interval: "1s"
  workflow:
    collect:
      metrics:
        /intel/smartmon/devices/*/*/num: {}
        /intel/smartmon/devices/*/*/raw: {}
        /intel/smartmon/devices/*/*/threshold: {}
        /intel/smartmon/devices/*/*/type: {}
        /intel/smartmon/devices/*/*/updated: {}
        /intel/smartmon/devices/*/*/value: {}
        /intel/smartmon/devices/*/*/whenfailed: {}
        /intel/smartmon/devices/*/*/worst: {}
      publish:
        -
          plugin_name: file
          config:
            file: /tmp/published_pysmart.out
EOF
```

  [Example (JSON) task manifest](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/blob/master/examples/tasks/task-smart.json) 

5.  Start task by running:
```
$ snaptel task create -t pysmart-file.yaml
Using task manifest to create task
Task created
ID: c6d095a6-733d-40cf-a986-9c82aa64b4e2
Name: Task-c6d095a6-733d-40cf-a986-9c82aa64b4e2
State: Running
```

  * List the task by running: 
```
$ snaptel task list
ID 					 NAME 						 STATE 		 HIT 	 MISS 	 FAIL 	 CREATED 		 LAST FAILURE
c6d095a6-733d-40cf-a986-9c82aa64b4e2 	 Task-c6d095a6-733d-40cf-a986-9c82aa64b4e2 	 Running 	 9 	 0 	 0 	 10:39AM 2-23-2017
```

  * Watch the task by running:
```
$ snaptel task watch c6d095a6-733d-40cf-a986-9c82aa64b4e2
```

  * Stop the task by running:
```
$ snaptel task stop c6d095a6-733d-40cf-a986-9c82aa64b4e2
Task stopped:
ID: c6d095a6-733d-40cf-a986-9c82aa64b4e2
```

![fig0](https://www.dropbox.com/s/tp24zyapu28gdkl/fig0.gif?raw=1)

### Roadmap
There isn't a current roadmap for this plugin, but it is in active development. As we launch this plugin, we do not have any outstanding requirements for the next release. If you have a feature request, please add it as an [issue](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/issues/new) and/or submit a [pull request](https://github.com/intelsdi-x/snap-plugin-collector-pysmart/pulls).

## Community Support
This repository is one of **many** plugins in **Snap**, a powerful telemetry framework. See the full project at http://github.com/intelsdi-x/snap To reach out to other users, head to the [main framework](https://github.com/intelsdi-x/snap#community-support)

## Contributing
We love contributions!

There's more than one way to give back, from examples to blogs to code updates. See our recommended process in [CONTRIBUTING.md](CONTRIBUTING.md).

## License
[Snap](http://github.com/intelsdi-x/snap), along with this plugin, is an Open Source software released under the Apache 2.0 [License](LICENSE).

And **thank you!** Your contribution, through code and participation, is incredibly important to us.
