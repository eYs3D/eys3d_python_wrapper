"""Callback-based streaming demo for eYs3D stereo cameras.

Demonstrates the callback pattern for receiving frames from the camera.
Each frame type (color, depth, IMU) has a dedicated callback function
that runs in a separate thread managed by the C++ SDK.

Usage:
    This demo is typically run from demo.py by selecting "callback_demo".
    It demonstrates:
    - Starting stream with callbacks
    - Pausing and resuming stream
    - Accessing IMU data associated with frames
    - Stopping and restarting stream

Callback Threading Model:
    Each callback runs in a thread pool managed by C++. Callbacks should:
    - Return quickly to avoid blocking the producer
    - Use thread-safe data structures for shared state

Frame Data Access Methods - Safe vs Unsafe:
    The Frame object provides two types of data access methods:

    SAFE methods (copy data, can be stored):
        - get_rgb_data() -> np.ndarray: Returns a COPY of RGB data.
          The returned array owns its memory and is safe to store/use later.
        - get_raw_data() -> np.ndarray: Returns a COPY of raw sensor data.
        - get_depth_ZD_value() -> np.ndarray: Returns a COPY of depth values.

    UNSAFE methods (zero-copy, must use immediately):
        - get_rgb_data_unsafe() -> np.ndarray: Zero-copy, points to Frame memory.
        - get_raw_data_unsafe() -> np.ndarray: Zero-copy, points to Frame memory.
        - get_depth_ZD_value_unsafe() -> np.ndarray: Zero-copy, points to Frame memory.

        WARNING: Unsafe methods return arrays that point directly to internal
        Frame buffers. The Frame may be recycled after callback returns,
        making the array data INVALID. Use unsafe methods only when:
        - You need maximum performance (no memory copy overhead)
        - You process the data immediately within the callback
        - You DO NOT store references to the returned arrays

    Example - Safe (recommended for most cases):
        def callback(frame):
            rgb = frame.get_rgb_data()  # Safe copy, can store
            self.last_frame = rgb       # OK to store

    Example - Unsafe (for performance-critical code):
        def callback(frame):
            rgb = frame.get_rgb_data_unsafe()  # Zero-copy
            cv2.imshow("preview", rgb)         # Process immediately
            # DO NOT store rgb - it becomes invalid after callback returns
"""

import sys
import time

import cv2
import numpy as np
import eys3d
import eys3dPy

from eys3d import Device, Pipeline, Config, COLOR_RAW_DATA_TYPE, DEPTH_RAW_DATA_TYPE

# FPS calculation constants (commented out in callbacks)
DURATION: int = 100
count: int = 0
timestamp: int = 0


def color_frame_callback(frame: eys3dPy.Frame) -> None:
    """Callback for color frames - demonstrates unsafe API with luminance computation.

    Uses get_rgb_data_unsafe() for zero-copy access and computes luminance
    statistics immediately within the callback. This is safe because we only
    use the data within the callback scope - no references are stored.

    Args:
        frame: eys3dPy.Frame object with the following key methods:
            - get_serial_number() -> int: Frame sequence number.
            - get_sensor_dataset() -> SensorDataSet: Associated IMU samples.
            - get_timestamp() -> int: Timestamp in microseconds.
            - get_width() / get_height() -> int: Frame dimensions.

            Safe methods (copy data, can store):
            - get_rgb_data() -> np.ndarray: RGB pixel data copy (H*W*3).
            - get_raw_data() -> np.ndarray: Raw YUY2 data copy.

            Unsafe methods (zero-copy, process immediately):
            - get_rgb_data_unsafe() -> np.ndarray: Direct pointer to RGB buffer.
            - get_raw_data_unsafe() -> np.ndarray: Direct pointer to raw buffer.
    """
    # Zero-copy access using unsafe API - process immediately, do not store
    bgr = frame.get_rgb_data_unsafe().reshape(
        frame.get_height(), frame.get_width(), 3)

    # Compute luminance: Y = 0.299*R + 0.587*G + 0.114*B
    # BGR order: B=channel 0, G=channel 1, R=channel 2
    luminance = np.mean(
        0.114 * bgr[:, :, 0] +  # B
        0.587 * bgr[:, :, 1] +  # G
        0.299 * bgr[:, :, 2]    # R
    )

    print(f"[Python][COLOR] S/N={frame.get_serial_number()}, luminance={luminance:.1f}")


def depth_frame_callback(frame: eys3dPy.Frame) -> None:
    """Callback for depth frames - demonstrates unsafe API with cv2.imshow.

    Uses get_rgb_data_unsafe() for zero-copy access and displays the depth
    heatmap immediately using OpenCV. This is thread-safe because only this
    callback calls cv2 functions (color callback only computes statistics).

    Args:
        frame: eys3dPy.Frame object with the following key methods:
            - get_serial_number() -> int: Frame sequence number.
            - get_timestamp() -> int: Timestamp in microseconds.
            - get_width() / get_height() -> int: Frame dimensions.

            Safe methods (copy data, can store):
            - get_depth_ZD_value() -> np.ndarray: Distance in mm copy (H*W, uint16).
            - get_rgb_data() -> np.ndarray: Colorized depth heatmap copy (H*W*3).
            - get_raw_data() -> np.ndarray: Raw 11/14-bit packed depth data copy.

            Unsafe methods (zero-copy, process immediately):
            - get_depth_ZD_value_unsafe() -> np.ndarray: Direct pointer to depth buffer.
            - get_rgb_data_unsafe() -> np.ndarray: Direct pointer to RGB heatmap buffer.
            - get_raw_data_unsafe() -> np.ndarray: Direct pointer to raw depth buffer.
    """
    # Zero-copy access using unsafe API - display immediately
    bgr = frame.get_rgb_data_unsafe().reshape(frame.get_height(), frame.get_width(), 3)

    # Display depth heatmap - cv2.imshow copies data internally
    cv2.imshow("Depth (unsafe API demo)", bgr)
    cv2.waitKey(1)

    print("[Python][DEPTH] S/N={}".format(frame.get_serial_number()))


def imu_data_callback(sensor_data: eys3dPy.SensorData) -> None:
    """Callback for IMU sensor data from SensorDataProducer.

    Called by C++ thread pool for each IMU sample batch.

    Args:
        sensor_data: eys3dPy.SensorData object with the following methods:
            - get_serial_number() -> int: Sample sequence number.
            - get_data() -> dict: IMU readings (accel, gyro, etc.).
            - get_type() -> SensorDataType: Sensor type identifier.
    """
    print("[Python][IMU] The S/N in callback function: {}".format(
        sensor_data.get_serial_number()))


def callback_sample(device: Device, config: Config) -> None:
    """Run the callback streaming demo.

    Demonstrates the callback-based streaming pattern:
    1. Start stream with color/depth/IMU callbacks (10 seconds)
    2. Pause stream (1 second)
    3. Resume stream (2 seconds)
    4. Stop and restart without callbacks (2 seconds)

    Args:
        device: Device instance to stream from.
        config: Stream configuration.

    Note:
        Total runtime is approximately 15 seconds.
    """
    pipe = Pipeline(device=device)
    conf = config

    device.open_device(conf,
                       colorFrameCallback=color_frame_callback,
                       depthFrameCallback=depth_frame_callback,
                       IMUDataCallback=imu_data_callback)
    device.enable_stream()
    print(
        "\n\n\n********[Python][INFO] Start stream with callback function********"
    )
    time.sleep(10)
    device.pause_stream()
    print("\n\n\n********[Python][INFO] Pause stream********")
    time.sleep(1)
    device.enable_stream()
    print("\n\n\n********[Python][INFO] Start previous stream********")
    time.sleep(2)
    device.close_stream()
    print("\n\n\n********[Python][INFO] Stop stream********")
    device.open_device(conf)
    print(
        "\n\n\n********[Python][INFO] Start stream without callback function********"
    )
    device.enable_stream()
    time.sleep(2)
    device.close_stream()
    cv2.destroyAllWindows()
    print("\n\n\n********[Python][INFO] Stop stream********")
