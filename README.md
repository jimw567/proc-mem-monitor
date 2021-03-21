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
![image](https://user-images.githubusercontent.com/24323762/111917693-a8d3f280-8a3e-11eb-885a-a261787acc54.png)