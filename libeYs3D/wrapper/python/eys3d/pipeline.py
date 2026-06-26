"""Pipeline module for polling-based frame retrieval.

Provides the Pipeline class for pull-based camera streaming as an alternative
to callback-based streaming via Device.open_device().

PIPELINE_RESULT Enum:
    Frame retrieval methods return eys3dPy.PIPELINE_RESULT values:

    - OK: Frame retrieved successfully.
    - TIMEOUT: No new frame within the specified timeout period.
    - QUEUE_EMPTY: No frame available (non-blocking poll only).
    - STOPPED: Pipeline has been stopped via stop() or pause().
    - SYNC_ERROR: Frame synchronization error (FrameSetPipeline only).
    - QUEUE_FULL: Internal queue overflow (should not occur in normal use).

    Example:
        ret, frame = pipe.wait_depth_frame(timeout=1000)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            process(frame)
        elif ret == eys3dPy.PIPELINE_RESULT.TIMEOUT:
            logger.warning("Frame timeout")
"""
import threading
import time
import numpy as np
from typing import Optional, Tuple, Dict
from eys3d import logger
import eys3dPy
from .device import Device
from .config import Config, ModeConfig
from .depthFilter import DepthFilterOptions
from .depthAccuracy import DepthAccuracy
from .cameraProperty import CameraProperty
from .irProperty import IRProperty


class Pipeline:
    """Pull-based frame retrieval with latest-wins semantics.

    Provides a polling interface for retrieving camera frames without callbacks.
    The C++ Pipeline uses LatestFrameBuffer, which always keeps only the most
    recent frame - older frames are silently discarded if not consumed in time.

    Best suited for:
    - UI/preview applications displaying at screen refresh rate
    - Algorithms that need current state, not frame history
    - Variable-rate consumers slower than camera frame rate

    The underlying C++ Pipeline provides:
    - LatestFrameBuffer for color/depth/PC (latest-wins, zero-copy swap)
    - CircularQueue for IMU data (FIFO, 8-sample buffer)
    - Thread-safe producer/consumer synchronization

    Args:
        device_index: Camera index (ignored if device is provided).
        device: Existing Device instance to use (preferred).

    Example:
        >>> device = Device(0)
        >>> config = Config()
        >>> config.set_preset_mode_config(0x0202, 1, 3)
        >>> pipe = Pipeline(device=device)
        >>> pipe.start(config)
        >>> while running:
        ...     ret, frame = pipe.wait_depth_frame(timeout=1000)
        ...     if ret:
        ...         process(frame)
        >>> pipe.stop()

    Note:
        Pre-allocates Frame buffers at start() to avoid resize overhead.
        The C++ LatestFrameBuffer swaps buffer pointers in O(1) time.
    """
    def __init__(self, device_index: int = 0, device: Optional[Device] = None) -> None:
        if device:
            self.__dev = device
        else:
            self.__dev = Device(device_index)
        self.__config = None
        self.__pipe = None
        self.dev_info = self.__dev.get_device_info()

        self.__color_frame_shape = None
        self.__depth_frame_shape = None

        self.__depth_accuracy_info = None
        self.__depth_zValue = None

        self.__status = False

        # Pre-allocated frames to avoid resize on every cloneOut
        self.__color_frame = None
        self.__depth_frame = None

    @logger.catch
    def start(self, config: Optional[Config] = None) -> None:
        """Start streaming with the given configuration.

        Opens the camera device and starts frame producer threads.
        Pre-allocates Frame buffers sized for the configured resolution
        to avoid reallocation overhead during streaming.

        Args:
            config: Stream configuration. Required on first call.

        Raises:
            Exception: If config is None and no previous config was set.

        Note:
            Frame pre-allocation sizes:
            - dataVec: width * height * 2 (YUY2/depth raw)
            - zdDepthVec: width * height (uint16 per pixel)
            - rgbVec: width * height * 3 (RGB888)
        """
        if config is None and self.__config is None:
            logger.exception("Config needed for device setting.")
            raise Exception("Config needed for device setting.")
        else:
            self.__config = config

        if not self.__status:
            self.__status = True
            self.__pipe = self.__dev.open_device_with_pipeline(
                config=self.__config, sync=False)
            self.__color_frame_shape = self.__config.get_color_stream_resolution()
            self.__depth_frame_shape = self.__config.get_depth_stream_resolution()

            # Pre-allocate frames with correct buffer sizes to avoid resize on cloneOut
            # Frame(dataBufferSize, initDataVal, zdDepthBufferSize, initZDDepthVal, rgbBufferSize, initRGBVal)
            color_w, color_h = self.__color_frame_shape if self.__color_frame_shape else (0, 0)
            depth_w, depth_h = self.__depth_frame_shape if self.__depth_frame_shape else (0, 0)

            if color_w > 0 and color_h > 0:
                color_pixels = color_w * color_h
                # YUY2 = 2 bytes/pixel, zdDepth = 1 uint16 per pixel, RGB = 3 bytes/pixel
                self.__color_frame = eys3dPy.Frame(
                    color_pixels * 2, 0,    # dataBufferSize, initDataVal
                    color_pixels, 0,        # zdDepthBufferSize, initZDDepthVal
                    color_pixels * 3, 0     # rgbBufferSize, initRGBVal
                )

            if depth_w > 0 and depth_h > 0:
                depth_pixels = depth_w * depth_h
                # Depth raw = 2 bytes/pixel, zdDepth = 1 uint16 per pixel, RGB = 3 bytes/pixel
                self.__depth_frame = eys3dPy.Frame(
                    depth_pixels * 2, 0,    # dataBufferSize, initDataVal
                    depth_pixels, 0,        # zdDepthBufferSize, initZDDepthVal
                    depth_pixels * 3, 0     # rgbBufferSize, initRGBVal
                )

        self.__dev.enable_color_depth_stream()

    @logger.catch
    def get_color_frame(self) -> Tuple[bool, Optional[eys3dPy.Frame]]:
        """Non-blocking poll for latest color frame.

        Returns immediately. If a new frame is available, clones it to the
        pre-allocated buffer and returns it. Uses LatestFrameBuffer semantics -
        only the most recent frame is kept.

        Returns:
            Tuple of (success, frame):
                - (True, Frame): New frame available
                - (False, None): No new frame (already consumed the latest)

        Note:
            Frame data is accessed via methods:
            - frame.get_rgb_data(): RGB888 array, reshape to (H, W, 3)
            - frame.get_raw_data(): Raw YUY2 data
            - frame.get_serial_number(): Frame sequence number
        """
        if self.__color_frame is None:
            return False, None
        ret = self.__pipe.get_color_frame(self.__color_frame)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, self.__color_frame
        else:
            logger.warning(
                "`get_color_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    @logger.catch
    def get_depth_frame(self) -> Tuple[bool, Optional[eys3dPy.Frame]]:
        """Non-blocking poll for latest depth frame.

        Returns immediately. If a new frame is available, clones it to the
        pre-allocated buffer and returns it.

        Returns:
            Tuple of (success, frame):
                - (True, Frame): New frame available
                - (False, None): No new frame (already consumed the latest)

        Note:
            Frame data is accessed via methods:
            - frame.get_rgb_data(): Colorized depth heatmap (H, W, 3)
            - frame.get_depth_ZD_value(): Distance in mm, reshape to (H, W)
            - frame.get_raw_data(): Raw depth data (11/14-bit packed)
        """
        if self.__depth_frame is None:
            return False, None
        ret = self.__pipe.get_depth_frame(self.__depth_frame)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, self.__depth_frame
        else:
            logger.warning(
                "`get_depth_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    @logger.catch
    def wait_color_frame(self, timeout: int = 1600) -> Tuple[bool, Optional[eys3dPy.Frame]]:
        """Blocking wait for next color frame.

        Waits until a new frame is produced or timeout expires.
        Uses LatestFrameBuffer - returns the most recent frame,
        intermediate frames are discarded.

        Args:
            timeout: Maximum wait time in milliseconds. Default 1600ms.
                - timeout > 0: Wait up to timeout ms
                - timeout == 0: Non-blocking (same as get_color_frame)
                - timeout < 0: Wait indefinitely (with 3.2s safety checks)

        Returns:
            Tuple of (success, frame):
                - (True, Frame): Frame received within timeout
                - (False, None): Timeout or pipeline stopped
        """
        if self.__color_frame is None:
            return False, None
        ret = self.__pipe.wait_color_frame(self.__color_frame, timeout)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, self.__color_frame
        else:
            logger.warning(
                "`wait_color_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    @logger.catch
    def wait_depth_frame(self, timeout: int = 1600) -> Tuple[bool, Optional[eys3dPy.Frame]]:
        """Blocking wait for next depth frame.

        Waits until a new frame is produced or timeout expires.
        Uses LatestFrameBuffer - returns the most recent frame.

        Args:
            timeout: Maximum wait time in milliseconds. Default 1600ms.

        Returns:
            Tuple of (success, frame):
                - (True, Frame): Frame received within timeout
                - (False, None): Timeout or pipeline stopped
        """
        if self.__depth_frame is None:
            return False, None
        ret = self.__pipe.wait_depth_frame(self.__depth_frame, timeout)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, self.__depth_frame
        else:
            logger.warning(
                "`wait_depth_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    def get_device(self) -> Device:
        """Get the underlying Device instance.

        Returns:
            Device object for advanced camera control.
        """
        return self.__dev

    def pause(self) -> None:
        """Pause all streams.

        Suspends frame producers but keeps device open.
        """
        self.__dev.pause_stream()

    def pause_color_depth_stream(self) -> None:
        """Pause color and depth streams only."""
        self.__dev.pause_color_depth_stream()

    def reset(self) -> None:
        """Reset internal frame buffers.

        Note: With LatestFrameBuffer design, this is typically not needed
        as the buffer automatically keeps only the latest frame.
        """
        self.__pipe.reset()

    def stop(self) -> None:
        """Stop streaming and close device.

        Stops all frame producers and releases USB device.
        Call start() to restart.
        """
        self.__status = False
        self.__dev.close_stream()

    def is_interleave_mode_enabled(self) -> bool:
        """Check if interleave mode is enabled.

        Returns:
            True if ILM is active (G120 eSP936 series chip).
        """
        return self.__dev.is_interleave_mode_enabled()

    def get_depthFilter_options(self) -> DepthFilterOptions:
        """Get depth filter configuration.

        Returns:
            DepthFilterOptions for spatial/temporal filtering.
        """
        return self.__dev.get_depthFilter_options()

    def get_depthAccuracy(self) -> DepthAccuracy:
        """Get depth accuracy measurement.

        Returns:
            DepthAccuracy for fill rate and precision metrics.
        """
        return self.__dev.get_depthAccuracy()

    def get_cameraProperty(self) -> CameraProperty:
        """Get camera property control.

        Returns:
            CameraProperty for exposure, white balance, etc.
        """
        return self.__dev.get_cameraProperty()

    def get_accuracy_info(self) -> Optional[Dict[str, float]]:
        """Get latest depth accuracy measurements.

        Returns:
            Dictionary containing (or None if not available):
                - distance: Measured distance (mm)
                - fill_rate: Percentage of valid depth pixels
                - z_accuracy: Depth accuracy percentage
                - temporal_noise: Frame-to-frame noise
                - spatial_noise: Pixel-to-pixel noise
                - angle: Surface angle
                - angle_x: X-axis angle
                - angle_y: Y-axis angle
        """
        return self.__depth_accuracy_info

    def get_IRProperty(self) -> IRProperty:
        """Get IR projector control.

        Returns:
            IRProperty for adjusting IR intensity.
        """
        return self.__dev.get_IRProperty()
