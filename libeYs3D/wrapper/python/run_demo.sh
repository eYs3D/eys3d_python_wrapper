#!/bin/bash
# Usage: sh run_demo.sh <module_pid> <mode_index> [depth_bits] [--imu]
# Example: sh run_demo.sh 0x0202 1 11
# Example with IMU: sh run_demo.sh 0x0181 1 11 --imu

VENDOR_SDK_ROOT=../../..
PYTHON_EXECUTE=$(which python3)
EYS3D_PYTHON_LIB="$VENDOR_SDK_ROOT/libeYs3D/wrapper/python"
export PYTHONPATH="$PYTHONPATH:$VENDOR_SDK_ROOT/libeYs3D/out:$EYS3D_PYTHON_LIB"

# C++ Engine config path
export EYS3D_HOME="$VENDOR_SDK_ROOT/libeYs3D/out/eYs3D"

# Python Engine config path
export EYS3D_SDK_HOME="$VENDOR_SDK_ROOT/libeYs3D/out/eYs3D"

# Check for --imu flag
USE_SUDO=""
for arg in "$@"; do
	if [ "$arg" = "--imu" ]; then
		USE_SUDO="sudo --preserve-env=PYTHONPATH --preserve-env=EYS3D_HOME --preserve-env=EYS3D_SDK_HOME"
	fi
done

# Build command
if [ -z $3 ] || [ "$3" = "--imu" ]; then
	$USE_SUDO $PYTHON_EXECUTE sample_code/demo.py -m $1 -i $2
else
	$USE_SUDO $PYTHON_EXECUTE sample_code/demo.py -m $1 -i $2 --depth-bit $3
fi

