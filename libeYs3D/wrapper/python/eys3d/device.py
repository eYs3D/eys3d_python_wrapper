import json
import numpy as np
from typing import Dict, Optional, Callable, Union, Any

import eys3dPy
from eys3d import logger
from .depthFilter import DepthFilterOptions
from .depthAccuracy import DepthAccuracy
from .cameraProperty import CameraProperty
from .irProperty import IRProperty
from .config import RectLogData
from .register import RegisterOptions

__all__ = ["Device"]


class EYS3DSystem:
    """eYs3D camera system manager (singleton).

    Initializes USB subsystem and enumerates connected eYs3D cameras.
    Uses singleton pattern to prevent USB reinitialization race conditions
    that can cause device detection failures.

    The C++ System class (eys3dPy.System) manages:
    - USB device enumeration via libusb
    - Camera device instantiation
    - Global configuration (color byte order)

    Example:
        >>> system = EYS3DSystem()
        >>> count = system.get_camera_device_count()
        >>> device = system.get_camera_device(0)
    """
    _instance: Optional['EYS3DSystem'] = None
    _system: Optional[eys3dPy.System] = None

    def __new__(cls) -> 'EYS3DSystem':
        if cls._instance is None:
            cls._instance = super(EYS3DSystem, cls).__new__(cls)
            cls._system = eys3dPy.System(eys3dPy.COLOR_BYTE_ORDER.COLOR_RGB24)
        return cls._instance

    @property
    def system(self) -> eys3dPy.System:
        """Get the underlying eys3dPy.System object."""
        return EYS3DSystem._system

    def get_camera_device(self, camera_index: int) -> Optional[eys3dPy.CameraDevice]:
        """Get camera device by index.

        Args:
            camera_index: Zero-based index of the camera (0 to count-1).

        Returns:
            eys3dPy.CameraDevice object, or None if no cameras found.
        """
        if self.get_camera_device_count() == 0:
            return None
        else:
            return self.system.get_camera_device(camera_index)

    def get_camera_device_count(self) -> int:
        """Get number of connected eYs3D cameras."""
        return self.system.get_camera_device_count()

    def dump_system_info(self) -> None:
        """Print system and device information to console/log."""
        self.system.dump_system_info()


class Device:
    """eYs3D camera device controller.

    High-level interface for controlling an eYs3D stereo camera.
    Wraps the C++ CameraDevice class to provide Python-friendly access to:
    - Stream control (start, pause, stop)
    - Frame callbacks (color, depth, point cloud, IMU)
    - Depth filtering and accuracy measurement
    - Camera/IR properties
    - Hardware post-processing (HWPP)
    - Rectification data access

    The underlying C++ CameraDevice manages:
    - USB communication via eSPDI SDK
    - Frame producers (separate threads for color/depth/PC)
    - ZD table lookup for depth-to-distance conversion
    - Interleave mode routing (G120 eSP936 series chip)

    Device State Machine:
        Valid operation sequences:

        Callback mode:
            open_device(config, callbacks) -> enable_stream() -> [streaming]
            [streaming] -> pause_stream() -> [paused]
            [paused] -> enable_stream() -> [streaming]
            [streaming/paused] -> close_stream() -> [closed]
            [closed] -> open_device() -> ... (restart)

        Pipeline mode:
            open_device_with_pipeline(config) -> enable_stream() -> [streaming]
            (same pause/resume/close as callback mode)

        Invalid sequences (undefined behavior):
            - enable_stream() before open_device()
            - close_stream() when already closed
            - open_device() without close_stream() first

    G120 (ORANGE Chip) Notes:
        - Interleave mode is auto-enabled based on depth format (0x18-0x1b)
        - Calling enable_interleave_mode() directly is unnecessary (ignored with warning)
        - Depth-only mode internally opens color endpoint at depth resolution

    Args:
        camera_index: Zero-based camera index. Use EYS3DSystem.get_camera_device_count()
            to determine available cameras.

    Raises:
        Exception: If no camera found at the specified index.

    Example:
        >>> device = Device(camera_index=0)
        >>> print(device.get_device_info())
        >>> device.open_device(config, colorFrameCallback=my_callback)
    """
    def __init__(self, camera_index: int = 0) -> None:
        self.__system = EYS3DSystem()
        self.__camera_device = self.__system.get_camera_device(camera_index)
        self.__camera_index = camera_index
        self.__rectLogIndex = 0

        if self.__camera_device is None:
            raise Exception("The depth camera device is not found")

    def dump_system_info(self) -> None:
        """Print system and device information to console/log."""
        self.__system.dump_system_info()

    def get_device_index(self) -> int:
        """Get the camera index this device was initialized with.

        Returns:
            Zero-based camera index.
        """
        return self.__camera_index

    @logger.catch
    def open_device(
        self,
        config: 'Config',
        rectLogIndex: int = 0,
        colorFrameCallback: Optional[Callable] = None,
        depthFrameCallback: Optional[Callable] = None,
        PCFrameCallback: Optional[Callable] = None,
        IMUDataCallback: Optional[Callable] = None
    ) -> None:
        """Open camera and start streaming with callbacks.

        Opens the USB device via APC_OpenDevice and starts frame producers.
        Each callback runs in a dedicated thread pool managed by C++.

        Args:
            config: Config object with stream settings (resolution, format, FPS).
            rectLogIndex: Rectification calibration file index (usually 0).
            colorFrameCallback: Called for each color frame. Signature:
                callback(frame: eys3dPy.Frame) -> bool
                Return True to continue, False to stop streaming.
            depthFrameCallback: Called for each depth frame. Same signature.
            PCFrameCallback: Called for each point cloud frame. Signature:
                callback(pcframe: eys3dPy.PCFrame) -> bool
            IMUDataCallback: Called for each IMU sample. Signature:
                callback(imu_data: eys3dPy.SensorData) -> bool

        Note:
            For G120 (eSP936 series chip) cameras with interleave mode enabled,
            color and depth frames alternate on the same endpoint. The C++
            ILMFrameRouter separates them by serial number parity.
        """
        try:
            conf = config.get_config()
        except Exception as e:
            raise e
        self.__rectLogIndex = conf['rectifyFileIndex']
        # open device whit init_stream
        self.__camera_device.init_stream(
            conf['colorFormat'],
            conf['colorWidth'],
            conf['colorHeight'],
            conf['actualFps'],
            conf['depthFormat'],
            conf['depthWidth'],
            conf['depthHeight'],
            conf['depthStreamFormat'],  # depthDataTransferCtrl
            eys3dPy.CONTROL_MODE.IMAGE_SN_SYNC,  # ctrlMode
            self.__rectLogIndex,  # #rectifyLogIndex
            colorFrameCallback,  # colorImageCallback
            depthFrameCallback,  # depthImageCallback
            PCFrameCallback,  # pcFrameCallback
            IMUDataCallback,  #IMUDataCallback
        )
        if conf['actualFps'] == conf['ILM']:
            self.__camera_device.enable_interleave_mode(True)
        else:
            self.__camera_device.enable_interleave_mode(False)

    def open_device_with_pipeline(
        self,
        config: 'Config',
        sync: int = 0
    ) -> 'eys3dPy.Pipeline':
        """Open camera and return a Pipeline for polling-based frame retrieval.

        Unlike open_device() which uses callbacks, this method returns a Pipeline
        object for pulling frames at the consumer's rate. Uses LatestFrameBuffer
        which keeps only the most recent frame - older frames are discarded.

        Args:
            config: Stream configuration (resolution, format, FPS).
            sync: Frame synchronization mode:
                - 0: Regular Pipeline (independent color/depth frames)
                - 1: FrameSetPipeline (synchronized color/depth/PC by serial number)

        Returns:
            eys3dPy.Pipeline (sync=0) with methods:
                - wait_color_frame(frame, timeout) -> PIPELINE_RESULT
                - wait_depth_frame(frame, timeout) -> PIPELINE_RESULT
                - wait_pc_frame(frame, timeout) -> PIPELINE_RESULT
                - get_color_frame(frame) -> PIPELINE_RESULT (non-blocking)
                - get_depth_frame(frame) -> PIPELINE_RESULT (non-blocking)
                - reset(): Clear internal buffers

            eys3dPy.FrameSetPipeline (sync=1) for synchronized frame sets.

        PIPELINE_RESULT enum values:
            - OK: Frame retrieved successfully
            - TIMEOUT: No frame within timeout period
            - QUEUE_EMPTY: No frame available (non-blocking poll)
            - STOPPED: Pipeline has been stopped
            - SYNC_ERROR: Frame synchronization error

        Note:
            For G120 (eSP936 series chip), interleave mode is automatically enabled
            based on the depth format in config. Calling enable_interleave_mode()
            directly is unnecessary (ignored with warning).

        Example:
            >>> pipe = device.open_device_with_pipeline(config, sync=0)
            >>> device.enable_stream()
            >>> ret = pipe.wait_color_frame(frame, timeout=1000)
            >>> if ret == eys3dPy.PIPELINE_RESULT.OK:
            ...     process(frame)
        """
        conf = config.get_config()
        if sync:
            pipeline = self.__camera_device.init_stream_with_frameset(
                conf['colorFormat'],
                conf['colorWidth'],
                conf['colorHeight'],
                conf['actualFps'],
                conf['depthFormat'],
                conf['depthWidth'],
                conf['depthHeight'],
                conf['depthStreamFormat'],  # depthDataTransferCtrl
                eys3dPy.CONTROL_MODE.IMAGE_SN_SYNC,  # ctrlMode
                conf['rectifyFileIndex'],  # #rectifyLogIndex
            )
        else:
            pipeline = self.__camera_device.init_stream(
                conf['colorFormat'],
                conf['colorWidth'],
                conf['colorHeight'],
                conf['actualFps'],
                conf['depthFormat'],
                conf['depthWidth'],
                conf['depthHeight'],
                conf['depthStreamFormat'],  # depthDataTransferCtrl
                eys3dPy.CONTROL_MODE.IMAGE_SN_SYNC,  # ctrlMode
                conf['rectifyFileIndex'],  # #rectifyLogIndex
            )
        if conf['actualFps'] == conf['ILM']:
            self.__camera_device.enable_interleave_mode(True)
        else:
            self.__camera_device.enable_interleave_mode(False)
        return pipeline

    def enable_stream(self) -> None:
        """Enable all streams (color, depth, and point cloud).

        Starts frame producer threads for all configured streams.
        """
        logger.info("Enable stream")
        self.__camera_device.enable_stream()

    def enable_PC_stream(self) -> None:
        """Enable point cloud streaming only.

        Starts the PCFrameProducer thread. Requires depth stream to be active.
        """
        logger.info("Enable PC stream")
        self.__camera_device.enable_pc_stream()

    def enable_color_depth_stream(self) -> None:
        """Enable color and depth streaming (no point cloud).

        Starts ColorFrameProducer and DepthFrameProducer threads.
        """
        logger.info("Enable stream")
        self.__camera_device.enable_color_depth_stream()

    def pause_stream(self) -> None:
        """Pause all streams temporarily.

        Suspends frame producers but keeps USB device open and callbacks registered.
        Use enable_stream() to resume.
        """
        logger.info("Pause stream")
        self.__camera_device.pause_stream()

    def pause_PC_stream(self) -> None:
        """Pause point cloud streaming only."""
        logger.info("Pause PC stream")
        self.__camera_device.pause_pc_stream()

    def pause_color_depth_stream(self) -> None:
        """Pause color and depth streams only."""
        logger.info("Pause stream")
        self.__camera_device.pause_color_depth_stream()

    def close_stream(self) -> None:
        """Close streams and release USB device.

        Stops all frame producers, closes USB device via APC_CloseDevice,
        and clears callbacks. Call open_device() to restart.
        """
        logger.info("Close stream")
        self.__camera_device.close_stream()

    def release(self) -> None:
        """Release device resources.

        Frees all resources associated with this device instance.
        The device object should not be used after calling release().
        """
        logger.info("Release stream")
        self.__camera_device.release()

    def get_device_info(self) -> Dict[str, Any]:
        """Get device identification and firmware information.

        Returns:
            Dictionary containing:
                - firmware_version: Firmware version string
                - serial_number: Device serial number
                - bus_info: USB bus information
                - mode_name: Model name string
                - dev_info: Nested dict with hardware details:
                    - PID: Product ID (e.g., 0x0202 for G120C)
                    - VID: Vendor ID (0x1e4e for eYs3D)
                    - dev_name: Device name string
                    - chip_ID: Chip identifier
                    - dev_type: Device type enum (GRAPE=5 for G120)
        """
        return self.__camera_device.get_camera_device_info()

    @logger.catch()
    def get_rectify_mat_log_data(self, nRectifyLogIndex: Optional[int] = None) -> RectLogData:
        """Get rectification calibration data.

        Args:
            nRectifyLogIndex: Rectification file index. If None, uses the index
                from the last open_device() call.

        Returns:
            RectLogData object containing camera intrinsic/extrinsic parameters.
        """
        if nRectifyLogIndex is None:
            nRectifyLogIndex = self.__rectLogIndex
        return RectLogData(self.__camera_device.get_rectify_log_data(),
                           nRectifyLogIndex)

    @logger.catch()
    def __get_zdtable_index(self) -> int:
        try:
            return eys3dPy.get_zdtable_index()
        except ValueError as e:
            raise e

    def get_usb_type(self) -> int:
        """Get USB port type as integer.

        Returns:
            3 for USB3.0, 2 for USB2.0, 0 for unknown.
        """
        usb_type = self.__camera_device.get_usb_port_type()
        if usb_type == eys3dPy.USB_PORT_TYPE.USB_PORT_TYPE_3_0:
            return 3
        elif usb_type == eys3dPy.USB_PORT_TYPE.USB_PORT_TYPE_2_0:
            return 2
        else:
            return 0  # USB_PORT_TYPE_UNKNOWN

    def get_z_range(self) -> Dict[str, int]:
        """Get depth Z range limits.

        Returns:
            Dict with 'Near' and 'Far' keys (in millimeters).
        """
        return self.__camera_device.get_z_range()

    def set_z_range(self, near: int, far: int) -> int:
        """Set depth Z range limits for filtering.

        Args:
            near: Minimum depth in millimeters.
            far: Maximum depth in millimeters.

        Returns:
            0 on success (APC_OK), error code otherwise.
        """
        return self.__camera_device.set_z_range(near, far)

    def get_depthFilter_options(self) -> DepthFilterOptions:
        """Get depth filter configuration interface.

        Returns:
            DepthFilterOptions for configuring spatial/temporal/edge filters.
        """
        return DepthFilterOptions(self.__camera_device)

    def get_depthAccuracy(self) -> DepthAccuracy:
        """Get depth accuracy measurement interface.

        Returns:
            DepthAccuracy for measuring fill rate, accuracy, and noise.
        """
        return DepthAccuracy(self.__camera_device)

    def get_cameraProperty(self) -> CameraProperty:
        """Get camera property control interface.

        Returns:
            CameraProperty for adjusting exposure, white balance, etc.
        """
        return CameraProperty(self.__camera_device)

    def get_IRProperty(self) -> IRProperty:
        """Get IR projector control interface.

        Returns:
            IRProperty for adjusting IR intensity and extended range.
        """
        return IRProperty(self.__camera_device)

    def get_register_options(self) -> RegisterOptions:
        """Get low-level register access interface.

        Returns:
            RegisterOptions for reading/writing hardware registers.
        """
        return RegisterOptions(self.__camera_device)

    def is_HWPP_supported(self) -> bool:
        """Check if hardware post-processing is supported.

        Returns:
            True if HWPP is available on this camera.
        """
        return self.__camera_device.is_HWPP_supported()

    def is_HWPP_enabled(self) -> bool:
        """Check if hardware post-processing is currently enabled.

        Returns:
            True if HWPP is active.
        """
        return self.__camera_device.is_HWPP_enabled()

    def enable_HWPP(self) -> None:
        """Enable hardware post-processing.

        HWPP applies on-chip depth filtering for improved quality.
        """
        self.__camera_device.enable_HWPP(True)

    def disable_HWPP(self) -> None:
        """Disable hardware post-processing."""
        self.__camera_device.enable_HWPP(False)

    def do_snapshot(self) -> None:
        """Capture and save current frames to disk.

        Saves color/depth frames to $EYS3D_HOME/snapshots/.
        """
        self.__camera_device.do_snapshot()

    def is_plyFilter_supported(self) -> bool:
        """Check if PLY point cloud filter is supported."""
        return self.__camera_device.is_plyFilter_supported()

    def enable_plyFilter(self) -> None:
        """Enable PLY point cloud filtering."""
        self.__camera_device.enable_plyFilter(True)

    def disable_plyFilter(self) -> None:
        """Disable PLY point cloud filtering."""
        self.__camera_device.enable_plyFilter(False)

    def is_plyFilter_enabled(self) -> bool:
        """Check if PLY filter is currently enabled."""
        return self.__camera_device.is_plyFilter_enabled()

    def is_interleave_mode_enabled(self) -> bool:
        """Check if interleave mode (ILM) is enabled.

        In interleave mode, color and depth frames alternate on a single
        USB endpoint. Used by G120 eSP936 series chip cameras.

        Returns:
            True if ILM is active.
        """
        return self.__camera_device.is_interleave_mode_enabled()

    def dump_frame_info(self, count: int = 60) -> None:
        """Dump frame timing and metadata for debugging.

        Saves frame information to $EYS3D_HOME/frames/.

        Args:
            count: Number of frames to record (default 60).

        Note:
            This operation takes time proportional to count.
        """
        self.__camera_device.dump_frame_info(count)

    def dump_IMU_data(self, count: int = 256) -> None:
        """Dump IMU sensor data for debugging.

        Saves IMU readings to $EYS3D_HOME/imu_log/.

        Args:
            count: Number of IMU samples to record (default 256).
        """
        self.__camera_device.dump_IMU_data(count)

    def get_IMU_device_info(self) -> Dict[str, Any]:
        """Get IMU sensor information.

        Returns:
            Dictionary containing:
                - VID: Vendor ID
                - PID: Product ID
                - type: IMU type identifier
                - serialNumber: Sensor serial number
                - fwVersion: Firmware version
                - moduleName: Module name string
                - status: Current status
                - isValid: Whether IMU is functional
        """
        return self.__camera_device.get_IMU_device_info()

    def set_depth_roi_center_point(self, x: int, y: int) -> None:
        """Set ROI center point for depth averaging.

        Args:
            x: X-coordinate of ROI center (pixels).
            y: Y-coordinate of ROI center (pixels).
        """
        self.__camera_device.set_depth_roi_center_point(x, y)

    def set_septh_roi_pixels(self, count: int) -> None:
        """Set ROI size for depth averaging.

        Args:
            count: ROI size in pixels (both width and height).
        """
        self.__camera_device.set_septh_roi_pixels(count)

    def dump_camera_device_properties(self) -> None:
        """Dump all camera device properties to log."""
        self.__camera_device.dump_camera_device_properties()

    def copy_from_G1toG2(self) -> None:
        """Copy calibration data from G1 to G2 (internal use)."""
        self.__camera_device.copy_from_G1toG2()
