# Feature
* Frame callback
* Pipeline
* Compatible with openCV
* Numpy supported 
* Preview Pointcloud with openGL.
* Support 8053, 8062
* Interleave mode 
* DepthFilter 
* Accuracy

# Prerequisite
* eYs3D camera module 

## Primary required software packages
* python3.7
* python3.7-venv
* eSPDI SDK
* cmake 3.20
* pkg-config

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
```

## OpenCL
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

## Configure Python Environment

### Create Python virtual environment
```console 
$ python3.7 -m venv ./pyEnv
$ source ./pyEnv/bin/activate 
```
Windows
```
pyEnv\Scripts\activate
```
If you want to exit python virtual environment <br>
```console
$ deactivate 
```

### install required Python packages with pip
```console
$ python3.7 -m pip install -r requirements.txt 
```

## make shared object Linux
> mkdir build && cd build  <br>
> cmake ../ -DSupport=general && make install -j16

## make shared object Linux for Python
> mkdir build && cd build  <br>
> cmake ../ && make install -j16

## Make log4cplus before building DLL Windows
> cd log4cplus\msvc14 <br>
> msbuild /P:Configuration=Release log4cplusS.vcxproj /p:CharacterSet=MBCS

## Make DLL Windows
> mkdir build && cd build  <br>
> cmake ..\ -G"Visual Studio 15 2017 Win64" -DSupport=general && msbuild /P:Configuration=Release INSTALL.vcxproj

## Make DLL Windows for Python
> mkdir build && cd build  <br>
> cmake ..\ -G"Visual Studio 15 2017 Win64" && msbuild /P:Configuration=Release INSTALL.vcxproj

# Save File 
> Default is at $HOME/.eYs3D
> If user want to specify save folder.
>```console
>export EYS3D_HOME="The directory user would like"
>```

## Snapshot 
> `$HOME/.eYs3D/snapshots`

## Log file. (Register)
> `$HOME/.eYs3D/logs`

## ModeConfig.db
> Please copy `ModeConfig.db` to `${EYS3D_HOME}/cfg` or `$HOME/.eYs3D`

## test function
> cd libeYs3D/wrapper/python <br>
> sh run_pytest.sh

# Getting the code

## Clone this repository with submodules
* git clone git@github.com:eYs3D/python-wrapper.git --recursiv

## Clone this repository and init submodules
* git clone git@github.com:eYs3D/python-wrapper.git
* git submodule init
* git submodule update --init --recursive

# Build the project
## In Windows environment
>     build OpenCV DLL: build.bat
>     build Unity DLL : build_unity.bat
## In Linux environment
```console
$ sh build.sh
```
## build the wrapper
```console
$ cmake .. -DCMAKE_CXX_FLAGS="-Wno-format-truncation -Wno-unused-result -O1 -g "
$ make install -j$(nproc)

# For Debugging PCFrame With SHA256
$ cmake .. -DCMAKE_CXX_FLAGS="-Wno-format-truncation -Wno-unused-result -O1 -g" -DPIPELINE_PCFRAME_SHA_DEBUG=1
$ make install -j$(nproc)
```
## make clean
``` console
$ cd libeYs3D/build
$ cmake --build . --target clean
```

# Code
## test function
```console 
$ cd libeYs3D/wrapper/python
$ sh run_pytest.sh [camera_module]
Ex: 
$ sh run_pytest.sh 8062
```
#### in Windows environment
> libeYs3D\run_callback.bat
> libeYs3D\run_frameset_pipeline.bat
> libeYs3D\run_pipeline.bat
#### in Linux environment
```console
$ cd libeYs3D
$ sh run_callback.sh
$ sh run_frameset_pipeline.sh
$ sh run_frameset_pipeline.sh
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
sh run_demo.sh 8062 1 
```

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
