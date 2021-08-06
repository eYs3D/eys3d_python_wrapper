### Feature
* Frame callback
* Pipeline
* Compatible with openCV
* Numpy supported 
* Preview Pointcloud with openGL.
* Support 8053, 8062
* Interleave mode 
* DepthFilter 
* Accuracy

### Getting the code

### Clone this repository with submodules
```git clone git@github.com:eYs3D/eys3d_python_wrapper.git```

### Prerequisite
* eYs3D camera module 

### Primary required software packages
* python3.7
* python3.7-venv
* eSPDI SDK
* cmake 3.20
* pkg-config
* libdc1394 package

```console
# Install required packages with the following command
$ sudo apt install python3.7
$ sudo apt-get install python3-pip
$ sudo apt-get install python3.7-venv
$ sudo apt install libpython3.7-dev
$ sudo apt-get install python3.7-dev
$ sudo apt install libx11-dev
$ sudo apt install libudev-dev
$ sudo apt install libglfw3
$ sudo apt install libglfw3-dev
$ sudo apt-get install libusb-1.0-0-dev
$ sudo apt install liblog4cplus-dev
$ sudo apt install cgroup-tools
$ sudo apt install libcgroup-dev
$ sudo apt install libssl-dev
$ sudo apt-get install -y libdc1394-22
```

### OpenCL
The following OpenCL packages on host machine are required for eYs3D python wrapper project
* ICD loader runtime
* Vendor specific compute runtime for openCL driver

### ICD loader runtime
Developers can directly use the ICD loader runtime available in eYs3D SDK (eSPDI/opencl/), and developers can also install the one which is available in Debian repository.
```console
$ sudo apt install ocl-icd-opencl-dev 
```

### Vendor specific compute runtime for openCL driver
Developers should check if GPU vendor specific compute runtime for openCL driver is installed properly on host machine, the following is an example of installing Intel graphics compute runtime for openCL driver.
```console 
$ sudo add-apt-repository ppa:intel-opencl/intel-opencl 
$ sudo apt update
$ apt install intel-opencl-icd 
```

### Verify OpenCL platform and devices available on the host
```console
$ sudo apt install clinfo
$ sudo clinfo
```

# Configure Python Environment

### Create Python virtual environment
```console 
$ python3.7 -m venv ./venv
$ source ./venv/bin/activate
```

### install required Python packages with pip
```console
$ python3.7 -m pip install -r requirements.txt 
```

## Run demo code
```console 
$ cd libeYs3D/wrapper/python
$ sh run_demo.sh [module_name] [mode_index] 
Then select index to execute sample code.
1. cv_demo 
2. pc_demo
3. callback_demo
4. accuracy_demo
5. record_playback_demo
```
ex: If your module is 8062, mode index 1 on ModeConfig.db.<br>
```console
sh run_demo.sh 8062 1 14
```

ex: If your module is 8071, mode index 1 on ModeConfig.db.<br>
```console
sh run_demo.sh HYPATIA 1 11
```

ex: If your module is 8067, mode index 1 on ModeConfig.db.<br>
```console
sh run_demo.sh 8067 1 11
```

ex: If your module is 8059, mode index 5 on ModeConfig.db.<br>
```console
sh run_demo.sh 8059 5 11
```

ex: If your module is 8036, mode index 1 on ModeConfig.db.<br>
```console
sh run_demo.sh 8036 1 14
```

ex: If your module is 8052, mode index 1 on ModeConfig.db.<br>
```console
sh run_demo.sh 8052 1 14
```

If you want to exit python virtual environment <br>
```console
$ deactivate 
```

# Save File
Default is at $HOME/.eYs3D
If user want to specify save folder.
```console
export EYS3D_HOME="The directory user would like"
```

## Snapshot
`$EYS3D_HOME/.eYs3D/snapshots`

## Log file. (Register)
`$EYS3D_HOME/.eYs3D/logs`

## ModeConfig.db
Please copy `ModeConfig.db` to `${EYS3D_HOME}/cfg` or `$HOME/.eYs3D`
### If user would like to set depth data type manually
Please read PIF and check which bit is acceptable in advance. 
```console
$ sh run_demo.sh [module_name] [mode_index] [depth_data_type]

ex: If your module is 8062, mode index 1 and depth_data_type 14 bits.
sh run_demo.sh 8062 1 14
```

### Depth Accuracy 
Please execute the `accuracy_demo` to calculate the quality of depth frame. <br>
User should decide the region ratio and ground truth distance in mm to calculate. <br>
Notice this function would not guarantee the performance.<br>


## Run Python-Cli
### Preview 
![Imgur](https://i.imgur.com/eeNXPrO.png)
### Code 
```console
$ cd libeYs3D/wrapper/python/eYs3Dcli
$ sh run_cli.sh
```
### Usage
* cd: Change directory.
* pwd: Print name of current/working directory.
* get_version: Version of eys3d package.
* get_module_info: The camera module information from device.
* set_fps: Set fps in manual. It is available in mode node.
* set_depth_bits: Set depth_data_type in manual. It is available in mode node.
* ls: List.
* (on the leaf) execute: Excute sample code.
* exit:  Exit python-cli 
```

## Testing pipeline implementation in libeYs3D
Please follow the instructions  to compile eYs3D.test for testing and verifying libeYs3D <br>
```console
$ cd libeYs3D && sh run_test.sh 

# Performance
## Monitor memory usage of eYs3D.test
```console
$ sudo pmap ${PID_OF_eYs3D.test} | tail -n 1
```

## Not showing up preview window in some OS
```console
Error: BadDrawable (invalid Pixmap or Window parameter) 9 Major opcode: 62 (X_CopyArea)Resource id: 0x3800056]
```
Please follow the instructions to add environment variable in your system.<br>
```console
sudo nano /etc/environment
```

Adding in the /etc/environment file.
```
QT_X11_NO_MITSHM=1
```
