# proc-mem-monitor
A Python Tkinter GUI for monitoring total memory usage of commands matching
specified pattern

# Installation
## OS
proc-mem-monitor has been tested on CentOS 7.8 and Ubuntu 16.04.

## Python
This program requires Python 3.6 or newer to run. 

### Ubuntu 16.04
The default Python on Ubuntu 16.04 is version 3.5. Run the commands below to 
install Python 3.6
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6 python3.6-venv python3.6-tk 
```

### Redhat/CentOS 7.8
The default Python on CentOS 7.8 is already version 3.6. You only need to 
install Python Tkinter.
```
sudo yum install python36-tkinter
```


## Create and activate a Python3 virtual environment
```
python3.6 -m venv venv
. venv/bin/activate
```

## Install required Python packages
`pip install -r requirements.txt`

## Install proc-mem-monitor
`python setup.py develop`

## Run xbutil-gui
`proc_mem_monitor`

# Snapshots
## Main window showing all commands matching the pattern
![image](https://user-images.githubusercontent.com/24323762/109429158-33c94c00-79af-11eb-9883-ba7668fa510d.png)

## Memory usage plot
![image](https://user-images.githubusercontent.com/24323762/109429189-5491a180-79af-11eb-930a-7346b6ae074f.png)

