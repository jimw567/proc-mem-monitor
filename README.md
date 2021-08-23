# Process Memory Monitor
A Python application for monitoring total memory usage of commands matching specified 
pattern. It displays the information either on Tkinter GUI if DISPLAY is availabe or
on stdout if it's launched from a text-only termainl.

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

## Install xbutil GUI as a regular user
`pip install proc_mem_monitor`

## Install xbutil GUI as a contributor
### Install required Python packages
`pip install -r requirements.txt`

### Install proc-mem-monitor in development Mode
`python setup.py develop`

# Run Process Memory Monitor
Run the command below from the Python virtual environment created above
`proc_mem_monitor`

# Snapshots
## Process Memory Monitor on Tkinter GUI
![image](https://user-images.githubusercontent.com/24323762/111917693-a8d3f280-8a3e-11eb-885a-a261787acc54.png)

# Publish xbutil_gui to PyPI
`./scripts/publish-pypi.sh`

The following modules may need to be upgraded or installed:
```
pip install --upgrade pip
pip install twine
```