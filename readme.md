# eYs3D Python Wrapper

A C++/Python library for eYs3D stereo camera modules providing real-time depth sensing and 3D imaging capabilities.

## Features

* Frame callback mode (push-based delivery)
* Pipeline mode (polling-based frame retrieval)
* FrameSet mode (synchronized color+depth delivery)
* OpenCV compatible
* NumPy array support
* Point cloud preview with OpenGL
* Interleave mode (ILM) support
* Depth filtering and accuracy measurement
* IMU sensor data access
* Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 support

### Supported Camera Modules

| Model | Product Name | Chip |
|-------|--------------|------|
| 8036 | G100 | eSP876 |
| 8052 | G50 | eSP876 |
| 8059 | R50 | eSP876 |
| 8062 | G100i | eSP876 |
| 8081 | G62 | eSP876 |
| 80362 | G100+ | eSP876 |
| 80363 | G120 | eSP936 |
| HYPATIA | G53 | eSP876 |
| HYPATIA2 | R77 | eSP876 |
| HYPATIA4 | R100 | eSP876 |
| Stacy | REF-B6 | eSP876 |
| StacyJunior | REF-B3 | eSP876 |

---

## Getting Started

### Prerequisites

* eYs3D camera module
* Python 3.7 or later
* python3-venv (or conda)

### Install Required System Packages

> **Note:** You can use conda instead of venv for virtual environment management.

```console
# Python virtual environment support
$ sudo apt install python3-venv python3-pip

# System libraries
$ sudo apt install libx11-dev libudev-dev
$ sudo apt install libglfw3 libglfw3-dev
$ sudo apt install libusb-1.0-0-dev
$ sudo apt install liblog4cplus-dev
$ sudo apt install cgroup-tools libcgroup-dev
$ sudo apt install libssl-dev
$ sudo apt install -y libdc1394-22
```

### OpenCL Setup (Optional)

OpenCL enables GPU-accelerated depth processing. The wrapper works without OpenCL, but GPU acceleration improves performance.

> **Note:** OpenCL installation varies by GPU vendor. The example below is for Intel integrated graphics. Refer to your GPU vendor's documentation for other platforms (NVIDIA, AMD, ARM Mali, etc.).

#### Example: Intel GPU

```console
# Install ICD loader
$ sudo apt install ocl-icd-opencl-dev

# Install Intel OpenCL runtime
$ sudo add-apt-repository ppa:intel-opencl/intel-opencl
$ sudo apt update
$ sudo apt install intel-opencl-icd

# Verify installation
$ sudo apt install clinfo
$ clinfo
```

---

## Python Environment Setup

### Create Virtual Environment

```console
$ python3 -m venv ./venv
$ source ./venv/bin/activate
```

### Install Python Dependencies

```console
$ pip install -r requirements.txt
```

### Exit Virtual Environment

```console
$ deactivate
```

---

## Running the Demo

### Quick Start

```console
$ cd libeYs3D/wrapper/python
$ sh run_demo.sh [module_pid] [mode_index] [depth_bits]
```

Select a demo from the menu:
1. `cv_demo` - OpenCV preview
2. `pc_demo` - Point cloud visualization
3. `callback_demo` - Frame callback example
4. `accuracy_demo` - Depth accuracy measurement

> **Tip:** Adjust IR level with M/m (increase) and N/n (decrease) for optimal depth quality.

### Usage Examples

**G120 (PID 0x0202) with 11-bit disparity mode:**
```console
$ lsusb
Bus 002 Device 008: ID 3438:0202 eYs3D YX80363

$ sh run_demo.sh 0x202 1 11
```

**G100+ (PID 0x0181) with 11-bit disparity mode:**
```console
$ lsusb
Bus 002 Device 013: ID 3438:0181 Etron Technology, Inc. HD Depth Camera

$ sh run_demo.sh 0x181 1 11
```

**R100 (PID 0x0204) with 14-bit distance mode:**
```console
$ lsusb
Bus 001 Device 091: ID 3438:0204 Etron Technology, Inc. HP-ASC-H201

$ sh run_demo.sh 0x204 1 14
```

---

## Demo Applications

### OpenCV Preview Demo (cv_demo)

Real-time color and depth preview using OpenCV.

![cv_demo screenshot](https://imgur.com/G5lhQZQ.png)

#### Hotkeys

| Key | Function |
|-----|----------|
| Q/q/Esc | Quit |
| E/e | Toggle Auto Exposure (AE) |
| W/w | Toggle Auto White Balance (AWB) |
| M/m | Increase IR level |
| N/n | Decrease IR level |
| I/i | Toggle extended IR range |
| P/p | Toggle Hardware Post-Processing (HWPP) |
| L/l | Increase depth ROI size |
| K/k | Decrease depth ROI size |
| 0 | Reset Z range to defaults |
| 1 | Set Z range (ZNear=1234, ZFar=5678) |
| 2 | Set Z range (ZNear=1200, ZFar=1600) |
| F1 | Save snapshot |
| F2 | Dump frame info |
| F3 | Dump IMU data |
| F4 | Dump system info |
| F5 | Save rectify log as JSON |
| F6 | Dump camera properties |

---

### Point Cloud Demo (pc_demo)

Interactive 3D point cloud visualization with OpenGL.

![pc_demo screenshot](https://imgur.com/lBuSmhS.png)

#### Hotkeys

| Key | Function |
|-----|----------|
| Q/q/Esc | Quit |
| M/m | Increase IR level |
| N/n | Decrease IR level |
| I/i | Toggle extended IR range |
| F/f | Toggle PLY filter |
| 0 | Reset Z range to defaults |
| 1 | Set Z range (ZNear=1234, ZFar=5678) |
| 2 | Set Z range (ZNear=1200, ZFar=1600) |
| F1 | Save snapshot |
| F2 | Dump frame info |
| F3 | Dump IMU data |
| F4 | Dump system info |
| F5 | Save rectify log |
| F6 | Dump camera properties |

#### Mouse Controls

| Action | Function |
|--------|----------|
| Scroll | Zoom in/out |
| Left click + drag | Rotate view |
| Double left click | Reset position |

---

## Python API Guide

### Callback Mode

Use callbacks for real-time frame processing with minimal latency. Best for applications requiring immediate frame processing.

```python
from eys3d import Device, Config

def color_frame_callback(frame):
    print(f"[COLOR] Serial: {frame.get_serial_number()}")
    # Process frame.get_rgb_data() here
    return True  # Return True to continue streaming

def depth_frame_callback(frame):
    print(f"[DEPTH] Serial: {frame.get_serial_number()}")
    # Process frame.get_depth_ZD_value() here
    return True

def callback_sample(device, config):
    device.open_device(config,
                       colorFrameCallback=color_frame_callback,
                       depthFrameCallback=depth_frame_callback)
    device.enable_stream()

    # ... streaming active ...

    device.pause_stream()   # Pause temporarily
    device.enable_stream()  # Resume
    device.close_stream()   # Stop and release
```

### Pipeline Mode (Polling)

Use pipeline mode for UI applications where frame timing is flexible. Provides non-blocking frame retrieval.

```python
import cv2
from eys3d import Device, Pipeline, Config

def pipeline_sample(device, config):
    pipe = Pipeline(device=device)
    pipe.start(config)

    # Wait for color frame
    ret, cframe = pipe.wait_color_frame()
    if ret:
        bgr_color = cframe.get_rgb_data().reshape(
            cframe.get_height(), cframe.get_width(), 3)
        cv2.imshow("Color", bgr_color)

    # Wait for depth frame
    ret, dframe = pipe.wait_depth_frame()
    if ret:
        bgr_depth = dframe.get_rgb_data().reshape(
            dframe.get_height(), dframe.get_width(), 3)
        cv2.imshow("Depth", bgr_depth)

        # Get Z values in millimeters
        z_map = dframe.get_depth_ZD_value().reshape(
            dframe.get_height(), dframe.get_width())

    pipe.stop()
```

---

## Configuration

### Environment Variables

Set `EYS3D_HOME` to specify the data storage directory. Default: `$HOME/.eYs3D`

```console
export EYS3D_HOME="/your/custom/path"
```

### Default Storage Paths

| Data Type | Path |
|-----------|------|
| Snapshots | `$EYS3D_HOME/snapshots` |
| Logs | `$EYS3D_HOME/logs` |
| Mode Config | `$EYS3D_HOME/cfg/ModeConfig.db` |

> **Note:** `ModeConfig.db` contains camera streaming parameters corresponding to the PIF (Product Information File) document.

### Manual Depth Data Type Selection

Refer to the PIF document to determine supported bit depths for your camera module.

```console
$ sh run_demo.sh [module_pid] [mode_index] [depth_bits]

# Example: G100i with 14-bit depth
$ sh run_demo.sh 0x181 1 14
```

---

## Depth Accuracy Measurement

Run `accuracy_demo` to measure depth frame quality metrics:

* **Fill rate** - Percentage of valid depth pixels
* **Z accuracy** - Depth measurement precision
* **Temporal noise** - Frame-to-frame stability
* **Spatial noise** - Within-frame consistency

Specify the ROI (Region of Interest) ratio and ground truth distance in millimeters.

> **Note:** Accuracy results are for reference only and do not guarantee production performance.

---

## Troubleshooting

### Preview Window Not Appearing

If you encounter this error:
```
Error: BadDrawable (invalid Pixmap or Window parameter) 9
Major opcode: 62 (X_CopyArea)
Resource id: 0x3800056
```

**Solution:** Add the following environment variable:

```console
$ sudo nano /etc/environment
```

Add this line:
```
QT_X11_NO_MITSHM=1
```

Then restart your session or reboot.

### Camera Not Detected

1. Check USB connection: `lsusb | grep -E "3438"`
2. Verify USB permissions: Add user to `video` group
   ```console
   $ sudo usermod -a -G video $USER
   $ newgrp video
   ```
3. Check if device is accessible: `ls -l /dev/video*`

---

## Additional Resources

* **API Documentation:** See `libeYs3D/wrapper/python/doc/` for detailed API reference
* **SDK Headers:** `eSPDI/eSPDI.h` and `eSPDI/eSPDI_def.h`
