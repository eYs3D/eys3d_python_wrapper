import json
import numpy as np

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
    """This class is to initialize eys3d system.

    This class is to initialize eys3d system.
    It creates a system and search eys3d camera module by query usb port.
    Then, it creates device instance by object.
    """
    def __init__(self):
        self.system = eys3dPy.System.get_eys3d_system()

    def get_camera_device(self, camera_index):
        """Get the eys3d camera device.

        To get the eys3d camera device.
        It could decide the camera by index.

        Args:
            camera_index (int): The index to select camera module.
        """
        if self.get_camera_device_count() == 0:
            return None
        else:
            return self.system.get_camera_device(camera_index)

    def get_camera_device_count(self):
        return self.system.get_camera_device_count()

    def dump_system_info(self):
        self.system.dump_system_info()


class Device(object):
    """The class is the function related to eys3d api function.

    The class is to control the eys3d api function.
    First, it creates the EYS3D system to control the device.
    Second, user could decide the camera module by index provided by EYS3D system.
    The device could control following function:
    * Stream
    * DepthFilter
    * Property
    * Register
    * Depth information

    Args:
        device_index (int): Index for device would like to initialize.
    """
    def __init__(self, camera_index=0):
        self.__system = EYS3DSystem()
        self.__camera_device = self.__system.get_camera_device(camera_index)
        self.__camera_index = camera_index
        self.__rectLogIndex = 0

        if self.__camera_device is None:
            raise Exception("The depth camera device is not found")

    def dump_system_info(self):
        self.__system.dump_system_info()

    def get_device_index(self):
        """Get the index of user-provided camera device.

        To get the index of user-provided camera device.

        Returns:
            int: The index of camera device.
        """
        return self.__camera_index

    @logger.catch
    def open_device(self,
                    config,
                    rectLogIndex=0,
                    colorFrameCallback=None,
                    depthFrameCallback=None,
                    PCFrameCallback=None,
                    IMUDataCallback=None):
        """Open camera device with Config and callback function.

        It would call APC_OpenDevice by stream setting.
        In the meantime, it also registers the callback function to get frame data.

        Args:
            config (obj): The Config class. It contains the streaming setting.
            colorFrameCallback (function): The callback function of color frame. User could define the callback function. If none, the device could not enable color streaming.
            depthFrameCallback (function): The callback function of depth frame. User could define the callback function. If none, the device could not enable depth streaming.
            PCFrameCallback (function): The callback function of point cloud frame. User could define the callback function. If none, the device could not enable point cloud streaming.
            IMUDataCallback (function): The callback function of IMU sensor data. User could define the callback function. If none, the device could not enable IMU streaming.
        """
        try:
            conf = config.get_config()
        except Exception as e:
            raise e
        self.__rectLogIndex = rectLogIndex
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

    def open_device_with_pipeline(self, config, sync=0):
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
                self.__rectLogIndex,  # #rectifyLogIndex
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
                self.__rectLogIndex,  # #rectifyLogIndex
            )
        if conf['actualFps'] == conf['ILM']:
            self.__camera_device.enable_interleave_mode(True)
        else:
            self.__camera_device.enable_interleave_mode(False)
        return pipeline

    def enable_stream(self):
        """Enable stream.

        To enable stream.
        It would enable color, depth and point cloud streaming.
        """
        logger.info("Enable stream")
        self.__camera_device.enable_stream()

    def pause_stream(self):
        """Pause stream

        To pause stream.
        The device would hold the resouce of config and callback function and then wait for next action.
        """
        logger.info("Pause stream")
        self.__camera_device.pause_stream()

    def close_stream(self, ):
        """Close stream

        To close stream.
        The device would close the stream then erase the config and callback.
        """
        logger.info("Close stream")
        self.__camera_device.close_stream()

    def release(self, ):
        """Release the device.

        The EYS3D system would release the device.
        """
        logger.info("Release stream")
        self.__camera_device.release()

    def get_device_info(self, ):
        """Get the device infomation.

        To get the device information from camera module as dictionary.
        It contains FW version, VID , PID and etc...

        Returns:
            dict: The device information. The key is following:
                * firmware_version
                * serial_number
                * bus_info
                * mode_name
                * dev_info
                    * PID
                    * VID
                    * dev_name
                    * chip_ID
                    * dev_type
        """
        return self.__camera_device.get_camera_device_info()

    @logger.catch()
    def get_rectify_mat_log_data(self, nRectifyLogIndex=None):
        if nRectifyLogIndex is None:
            nRectifyLogIndex = self.__rectLogIndex
        return RectLogData(self.__camera_device.get_rectify_log_data(),
                           nRectifyLogIndex)  #nRectifyLogIndex)

    @logger.catch()
    def __get_zdtable_index(self):
        try:
            return eys3dPy.get_zdtable_index()
        except ValueError as e:
            raise e

    def get_usb_type(self, ):
        usb_type = self.__camera_device.get_usb_port_type()
        if usb_type == eys3dPy.USB_PORT_TYPE.USB_PORT_TYPE_3_0:
            return 3
        elif usb_type == eys3dPy.USB_PORT_TYPE.USB_PORT_TYPE_2_0:
            return 2
        else:
            return 0  # eys3dPy.USB_PORT_TYPE.USB_PORT_TYPE_UNKNOW

    def get_z_range(self):
        return self.__camera_device.get_z_range()

    def set_z_range(self, near, far):
        return self.__camera_device.set_z_range(near, far)

    def get_depthFilter_options(self, ):
        """Get the class of DepthFilterOptions.

        To get the class of DepthFilterOptions.
        User could read description on `depthFilter` in detail.
        """
        return DepthFilterOptions(self.__camera_device)

    def get_depthAccuracy(self, ):
        """Get the class of DepthAccuracy.

        To get the class of DepthAccuracy.
        User could read description on `depthAccuracy` in detail.
        """
        return DepthAccuracy(self.__camera_device)

    def get_cameraProperty(self, ):
        """Get the class of CameraProperty.

        To get the class of CameraProperty.
        User could read description on `cameraProperty.py` in detail.
        """
        return CameraProperty(self.__camera_device)

    def get_IRProperty(self, ):
        return IRProperty(self.__camera_device)

    def get_register_options(self):
        return RegisterOptions(self.__camera_device)

    def is_HWPP_supported(self):
        """Return support status.

        To return spport status

        Returns:
            bool: The return value. True for enable, False otherwise.
        """
        return self.__camera_device.is_HWPP_supported()

    def is_HWPP_enabled(self):
        """Return the status of HWPP.

        Return the status of HWPP.

        Returns:
            bool: The return value. True for enable, False otherwise.
        """

        return self.__camera_device.is_HWPP_enabled()

    def enable_HWPP(self):
        """Enable HWPP.

        To enable HWPP.
        """

        self.__camera_device.enable_HWPP(True)

    def disable_HWPP(self):
        """Disable HWPP.

        To Disable HWPP.
        """

        self.__camera_device.enable_HWPP(False)

    def do_snapshot(self):

        self.__camera_device.do_snapshot()

    def is_plyFilter_supported(self):

        return self.__camera_device.is_plyFilter_supported()

    def enable_plyFilter(self):
        self.__camera_device.enable_plyFilter(True)

    def disable_plyFilter(self):
        self.__camera_device.enable_plyFilter(False)

    def is_plyFilter_enabled(self):
        return self.__camera_device.is_plyFilter_enabled()

    def is_interleave_mode_enabled(self):
        """Get the status of interleaveMode.

        To get the status of interleaveMode.

        Returns:
            bool: The return value. True for enable, False otherwise.
        """
        return self.__camera_device.is_interleave_mode_enabled()

    def dump_frame_info(self, count=60):
        """Dump frame information.

        Dump frame information to `~/.eYs3D/frames`.
        Notice:
            It needed a time to write log when called.

        Args:
            count (int): This is amount of recorded data.Default is 60.
        """
        self.__camera_device.dump_frame_info(count)

    def dump_IMU_data(self, count=256):
        """Dump IMU data.

        Dump IMU data.
        Default is `~/.eYs3D/imu_log`.

        Args:
            count (int): This is amount of recorded data.
        """
        self.__camera_device.dump_IMU_data(count)

    def get_IMU_device_info(self):
        """Get the information of IMU device.

        To get the information of IMU device.

        Return:
            dict: The information of IMU device. The key is following:
                * VID
                * PID
                * type
                * serialNumber
                * fwVersion
                * moduleName
                * status
                * isValid
        """
        return self.__camera_device.get_IMU_device_info()

    def set_depth_roi_center_point(self, x, y):
        """Set center (x, y) to calculate average z value.
        
        To set center (x, y) to calculate average z value.

        Args:
            x (int): The x-coordinate of ROI-center.
            y (int): The y-coordinate of ROI-center.
        """
        self.__camera_device.set_depth_roi_center_point(x, y)

    def set_septh_roi_pixels(self, count):
        """The count of pixel to calculate.

        To set the count of valuable pixel to calculate.

        count (int): The count of valuable pixel to calculate.
        """
        self.__camera_device.set_septh_roi_pixels(count)

    def dump_camera_device_properties(self):
        """
        """
        self.__camera_device.dump_camera_device_properties()
