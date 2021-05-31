import threading

import time
import numpy as np

from eys3d import logger
import eys3dPy
from .device import Device
from .config import Config, ModeConfig


class Pipeline():
    """This class is to manage the color, depth and point cloud stream with pipeline process.

    This class is to manage the color, depth and point cloud stream with pipeline process.
    The purpose is for easier device operation.
    User could start pipeline with user-defined callback function.

    Notice:
        It will call get_color_frame and get_depth_frame if user start with user-defined callback function.

    Args:
        device_index (int): Index for device would like to initialize.
    """
    def __init__(self, device_index=0, device=None):
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

    @logger.catch
    def start(self, config=None):
        """Start the stream with configure and callback function.

        To start the stream with configure and callback function.
        It would use the default callback function to get frame data of color and depth if callback function is None.

        Args:
            config (obj): The class Config.

        """
        if config is None and self.__config is None:
            logger.exception("Config needed for device setting.")
            raise Exception("Config needed for device setting.")
        else:
            self.__config = config

        if not self.__status:
            self.__status = True
            self.__pipe = self.__dev.open_device_with_pipeline(
                config=self.__config, )
            self.__color_frame_shape = self.__config.get_color_stream_resolution(
            )
            self.__depth_frame_shape = self.__config.get_depth_stream_resolution(
            )

        self.__dev.enable_stream()

    @logger.catch
    def get_color_frame(self, ):
        """Get the color frame from pipeline in C/C++.

        To retrive the depth frame from pipeline in C/C++ directly.
        It would return False if frame is not ready in queue of pipeline.
        It show rgb frame if raw_data is False, otherwise is raw data.
        The shape of rgb frame data is (H, W, 3).
        The shape of raw frame data is (H, W, 2).

        Returns:
            bool : The return value is to mean the frame data is ready or not.
            np.array : The array of frame data. The shape is (H, W, 3) if rgb data. The shape is (H, W, 2) if raw data.
        """
        frame = eys3dPy.Frame(0, 0, 0)
        ret = self.__pipe.get_color_frame(frame)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, frame
        else:
            logger.warning(
                "`get_color_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    @logger.catch
    def get_depth_frame(self, ):
        """Get the depth frame from pipeline in C/C++.

        To retrive the depth frame from pipeline in C/C++ directly.
        It would return False if frame is not ready in queue of pipeline.
        The shape of rgb frame data is (H, W, 3).
        The shape of raw frame data is (H, W, 2).

        Returns:
            bool : The return value is to mean the frame data is ready or not.
            np.array : The array of frame data. The shape is (H, W, 3) if rgb data. The shape is (H, W, 2) if raw data.
        """
        frame = eys3dPy.Frame(0, 0, 0)
        ret = self.__pipe.get_depth_frame(frame)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, frame
        else:
            logger.warning(
                "`get_depth_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    @logger.catch
    def wait_color_frame(self, timeout=1600):
        """Wait for color frame from queue.

        To retrieve head of color frame from queue in pipeline in C/C++.
        It would wait frame for few milliseconds user defined if queue is empty.

        The unit of timeout is milliseconds.

        Args:
            timeout (int): The maximun of time in milliseconds to wait. Default is 1600.
        
        Returns:
            bool : The return value is to mean the frame data is ready or not.
            np.array : The array of frame data. The shape is (H, W, 3) if rgb data. The shape is (H, W, 2) if raw data.
        """
        frame = eys3dPy.Frame(0, 0, 0)
        ret = self.__pipe.wait_color_frame(frame, timeout)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, frame
        else:
            logger.warning(
                "`wait_color_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    @logger.catch
    def wait_depth_frame(self, timeout=1600):
        """Wait for depth frame from queue.

        To retrieve head of depth frame from queue in pipeline in C/C++.
        It would wait frame for few milliseconds user defined if queue is empty.

        The unit of timeout is milliseconds.

        Args:
            timeout (int): The maximun of time in milliseconds to wait. Default is 1600.
        
        Returns:
            bool : The return value is to mean the frame data is ready or not.
            np.array : The array of frame data. The shape is (H, W, 3) if rgb data. The shape is (H, W, 2) if raw data.
        """

        frame = eys3dPy.Frame(0, 0, 0)
        ret = self.__pipe.wait_depth_frame(frame, timeout)
        if ret == eys3dPy.PIPELINE_RESULT.OK:
            return True, frame
        else:
            logger.warning(
                "`wait_depth_frame` is failed. The return value = {}.".format(
                    eys3dPy.PIPELINE_RESULT(ret)))
            return False, None

    def get_device(self):
        """Get the camera device.

        To get the camera device for operating the device in detail.

        Returns:
            obj : The class Device.
        """
        return self.__dev

    def pause(self):
        """Pause the stream.

        To pause the stream.
        """
        self.__dev.pause_stream()

    def reset(self, ):
        self.__pipe.reset()

    def stop(self, ):
        """Stop the stream.

        To stop the stream and then release device.
        """
        self.__status = False
        self.__dev.close_stream()

    def is_interleave_mode_enabled(self):
        """Get the status of interleaveMode.

        To get the status of interleaveMode.

        Returns:
            bool: The return value. True for enable, False otherwise.
        """
        return self.__dev.is_interleave_mode_enabled()

    def get_depthFilter_options(self, ):
        """Get the class of DepthFilterOptions.

        To get the class of DepthFilterOptions.
        User could read description on `depthFilter` in detail.

        Returns:
            obj : The class DepthFilter.
        """
        return self.__dev.get_depthFilter_options()

    def get_depthAccuracy(self, ):
        """Get the class of DepthAccuracy.

        To get the class of DepthAccuracy.
        User could read description on `depthAccuracy` in detail.

        Returns:
            obj : The class DepthAccuracy.
        """
        return self.__dev.get_depthAccuracy()

    def get_cameraProperty(self, ):
        """Get the class of CameraProperty.

        To get the class of CameraProperty.
        User could read description on `cameraProperty.py` in detail.

        Returns:
            obj : The class CameraProperty.
        """
        return self.__dev.get_cameraProperty()

    def get_accuracy_info(self):
        """Get the information of accruracy.

        To get the information of accuracy as dictionary.

        Returns:
           dict : The dictionary contains the information of accuracy. The key is following:
               * distance
               * fill_rate
               * z_accuracy
               * temporal_noise
               * spatial_noise
               * angle
               * angle_x
               * angle_y
        """
        return self.__depth_accuracy_info

    def get_IRProperty(self):
        return self.__dev.get_IRProperty()
