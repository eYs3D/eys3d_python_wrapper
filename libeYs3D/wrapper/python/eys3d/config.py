import os
import numpy as np
import json

import eys3dPy
from eys3d import logger, COLOR_RAW_DATA_TYPE, DEPTH_TRANSFER_CTRL, DEPTH_RAW_DATA_TYPE, USB_PORT_TYPE
from .utils import get_EYS3D_HOME


class Config():
    """This class is to set the configuration of streaming.

    This class is to set the configuration of streaming.
    It could set the resolution and format of color and depth frame.
    """
    def __init__(self, ):

        self.colorStreamFormat = COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2
        self.depthStreamFormat = DEPTH_TRANSFER_CTRL.DEPTH_IMG_COLORFUL_TRANSFER
        self.depthDataType = 0
        self.ep0Width = 0
        self.ep0Height = 0
        self.ep1Width = 0
        self.ep1Height = 0
        self.ep0fps = 0
        self.ep1fps = 0
        self.interleavefps = 0
        self.rectify = False

    def set_color_stream(self, streamFormat, nEP0Width, nEP0Height, fps):
        """Set the format and resolution of color stream.

        To set the format, resolution, and fps of color stream.
        Please refer PIF of camera module or ModeConfig.db.

        Args:
            streamFormat (int): The format of color stream. 0: YUY2. 1: MJPG.
                User could refer COLOR_RAW_DATA_YUY2 and COLOR_RAW_DATA_MJPG in COLOR_RAW_DATA_TYPE.
            nEP0Width (int): The width of the color stream.
            nEP0Height (int): The height of the color stream.
            fps (int): The fps of color stream.
        """
        self.colorStreamFormat = streamFormat
        self.ep0Width = nEP0Width
        self.ep0Height = nEP0Height
        self.ep0fps = fps

    def set_depth_stream(self, streamFormat, nEP1Width, nEP1Height, fps):
        """Set the format and resolution of depth stream.

        To set the format, resolution, and fps of depth stream.
        Please refer PIF of camera module or ModeConfig.db.

        Args:
            streamFormat (int): The format of depth stream. User could refer DEPTH_TRANSFER_CTRL.
                0: DEPTH_IMG_NON_TRANSFER, 1: DEPTH_IMG_GRAY_TRANSFER, 2: DEPTH_IMG_COLORFUL_TRANSFER.
            nEP0Width (int): The width of the depth stream.
            nEP0Height (int): The height of the depth stream.
            fps (int): The fps of depth stream.
        """
        self.depthStreamFormat = streamFormat
        self.ep1Width = nEP1Width
        self.ep1Height = nEP1Height
        self.ep1fps = fps

    def set_depth_data_type(self, depth_data_type):
        """Set the data type of depth stream.

        To set the data type for depth stream.
        It is avaliable for 8, 11, 14.
        
        Args:
            depth_data_type (int): The depth_data_type(bit) for eYs3D depth camera. 
                It could support 8, 11, 14 bit based on camera module. Please refer PIF.
        """
        if depth_data_type not in (0, 8, 11, 14):
            raise Exception(
                "depth_data_type is out of range. Please refer document")
        self.depthDataType = self.__DepthDataToFormatType(depth_data_type)

    def set_depth_data_type_with_advanced_setting(self, depth_data_type, is_rectify, is_interleave_mode):
        """Set the data type, rectified and interleave mode.

        This function is for user want to set config in manual
        Because the depth data type is related to rectified and interleave mode.

        Args:
            depth_data_type (int): Refer set_depth_data_type.
            is_rectify (bool): Rectified mode.[EYS3D][TODO]
            is_interleave_mode (bool): Interleave mode. [EYS3D][TODO]
        """
        if is_rectify:
            self.enable_rectify()
        else:
            self.disable_rectify()
        if is_interleave_mode:
            self.interleavefps = self.ep0fps if self.ep0fps else self.ep1fps
        self.set_depth_data_type(depth_data_type)

    def set_fps(self, fps):
        """Set the fps in manual.

        To set the fps in manual.

        Args:
            fps(int): The fps for depth camera.
        """
        self.ep1fps = self.ep0fps = fps

    def get_config(self):
        """Get the dictionary of the user-provided config.

        To get the dictionary of the user-provided config.

        Returns:
            dict: The user-provided config. The key is following:
                * colorFormat: The format of color stream.
                * colorWidth: The width of color stream.
                * colorHeight: The height of color stream.
                * depthStreamFormat: The format of depth stream.
                * depthWidth: The width of depth stream.
                * depthHeight: The width of depth stream.
                * actualFps: The actual fps.
                * depthFormat: The depth data type.
        """
        actualFps = self.ep0fps if self.ep0fps else self.ep1fps
        conf = dict({
            "colorFormat": self.colorStreamFormat,
            "colorWidth": self.ep0Width,
            "colorHeight": self.ep0Height,
            "depthStreamFormat": self.depthStreamFormat,
            "depthWidth": self.ep1Width,
            "depthHeight": self.ep1Height,
            "actualFps": actualFps,
            "depthFormat": self.depthDataType,  #bits 
            "ILM": self.interleavefps,
            "rectify": self.rectify,
        })

        return conf

    def get_color_stream_resolution(self):
        """Get the resolution of color stream.

        Get the resolution of color frame.
        The return order is height, width.

        Returns:
            tuple: The tuple contains height and width.
        """
        return (self.ep0Height, self.ep0Width)

    def get_depth_stream_resolution(self):
        """Get the resolution of depth stream.

        Get the resolution of depth frame.
        The return order is height, width.

        Returns:
            tuple: The tuple contains height and width.
        """
        return (self.ep1Height, self.ep1Width)

    def set_preset_mode_config(
        self,
        pid,
        index,
        usb_type,
    ):
        """Set the preset mode config.

        This function is to make the mode config setting easier. 
        User could select mode index from modeConfig.db to complete config setting.

        Args:
            pid (int): The product id of camera module. Please refer the PIF. It is availabel for integer or heximal.
            index (int): The mode index in modeConfig.db. 
        """
        modeConfig = ModeConfig(pid, index, usb_type)
        mode_info = modeConfig.get_current_mode_info()
        self.__update_config(mode_info, pid)

    def enable_rectify(self):
        self.rectify = True

    def disable_rectify(self):
        self.rectify = False

    def __update_config(self, mode_info, pid):
        self.pid = pid
        self.colorStreamFormat = COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2 if mode_info.eDecodeType_L == 0 else COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_MJPG
        self.ep0Height = mode_info.L_Resolution.Height
        self.ep0Width = mode_info.L_Resolution.Width
        self.ep1Height = mode_info.D_Resolution.Height
        self.ep1Width = mode_info.D_Resolution.Width
        self.ep0fps = 0 if not mode_info.vecColorFps else mode_info.vecColorFps[
            0]
        self.ep1fps = 0 if not mode_info.vecDepthFps else mode_info.vecDepthFps[
            0]
        self.interleavefps = mode_info.iInterLeaveModeFPS
        if mode_info.bRectifyMode:
            self.enable_rectify()
        else:
            self.disable_rectify()
        self.depthDataType = self.__DepthDataToFormatType(
            mode_info.
            vecDepthType[0] if len(mode_info.vecDepthType) != 0 else 0)

    def __DepthDataToFormatType(
        self,
        DepthData,
    ):
        DEPTH_RAW_DATA_INTERLEAVE_MODE_OFFSET = 16  # refer video.h:28
        DEPTH_RAW_DATA_SCALE_DOWN_MODE_OFFSET = 32  # refer video.h:28
        if DepthData == 8:
            depth_data_bit = DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_8_BITS if self.rectify else DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_8_BITS_RAW
        elif DepthData == 11:
            depth_data_bit = DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_11_BITS if self.rectify else DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_11_BITS_RAW
        elif DepthData == 14:
            depth_data_bit = DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_14_BITS if self.rectify else DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_14_BITS_RAW
        elif DepthData == 0:
            depth_data_bit = DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_OFF_RECTIFY if self.rectify else DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_OFF_RAW
        else:  # Default
            depth_data_bit = DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_DEFAULT if self.rectify else DEPTH_RAW_DATA_TYPE.DEPTH_RAW_DATA_OFF_RECTIFY

        if (self.pid == 0x120 or self.pid == 0x137) and 360 == self.ep1Height:  # This block for 8036/8052 scale down mode
            depth_data_bit = int(depth_data_bit) + DEPTH_RAW_DATA_SCALE_DOWN_MODE_OFFSET
            depth_data_bit = eys3dPy.DEPTH_RAW_DATA_TYPE(depth_data_bit)
        if self.pid == 0x173 and 460 == self.ep1Height:  # This block for Hypatia2 scale down mode
            depth_data_bit = int(depth_data_bit) + DEPTH_RAW_DATA_SCALE_DOWN_MODE_OFFSET
            depth_data_bit = eys3dPy.DEPTH_RAW_DATA_TYPE(depth_data_bit)
        if self.interleavefps == (self.ep0fps if self.ep0fps else self.ep1fps):  # ILM
            depth_data_bit = int(depth_data_bit) + DEPTH_RAW_DATA_INTERLEAVE_MODE_OFFSET
            depth_data_bit = DEPTH_RAW_DATA_TYPE(depth_data_bit)

        return depth_data_bit


class ModeConfig():
    """This class is to link database `modeConfig.db`.

    This class is to link database `modeConfig.db`.

    Args:
        pid (hex): The product id of camera module. Please refer the PIF.
        index (int): The mode index in modeConfig.db. 
        
    """
    def __init__(self, pid, index, usb_type):
        # it's no meaning but just pass a argument.
        self.__usb_type = USB_PORT_TYPE.USB_PORT_TYPE_3_0 if usb_type == 3 else USB_PORT_TYPE.USB_PORT_TYPE_2_0
        self.__pid = pid
        self.__maxIndex = 0
        self.__index = index

        try:
            self.__modeConfig = eys3dPy.ModeConfigOptions(self.__usb_type, pid)
            self.__maxIndex = self.__modeConfig.get_mode_count()
        except Exception as e:
            logger.exception(e)
            raise e
        if self.__modeConfig.select_current_index(
                self.__index) != 0:  # 0 is APC_OK in eSPDI_def.h
            self.__index = self.__modeConfig.get_current_index()
            logger.warning(
                "Alert!!Index is not in database. Default is the first config setting."
            )
        self.__mode_info = self.__modeConfig.get_current_mode_info()

    def get_current_index(self):
        """Get the index of current mode.

        To get the index of current mode.

        Returns:
            int: The index of current mode.
        """
        current_index = self.__modeConfig.get_current_index()
        self.__index = current_index
        return self.__index

    def get_current_mode_info(self):
        """Get the information of current mode.

        To get the information of current mode.
        It return a object of `MODE_CONFIG`.

        Returns:
            obj: The MODE_CONFIG. It contains 
                * iMode
                * iUSB_Type
                * iInterLeaveModeFPS
                * eDecodeType_L
                * eDecodeType_K
                * eDecodeType_T
                * L_Resolution
                * D_Resolution
                * K_Resolution
                * T_Resolution
                * vecDepthType
                * vecColorFps
                * vecDepthFps
        """
        return self.__mode_info

    def get_mode_count(self):
        """Get the total number of mode in modeConfig.db.

        To the the total number of mode on camera module in modeConfig.db.
        """
        return self.__maxIndex

    def get_modes(self):
        """Get the modes.

        To Get the modes.
        It is not to be implemented.

        Raise:
            NotImplementedError:
        """
        raise NotImplementedError

    @logger.catch()
    def select_current_index(self, index):
        """Select the index that user wanted.

        To select the index that user wanted.
        It raised error if index is not in modeConfig.db.

        Args:
            index (int): The index user wanted to select.

        Raises:
            IndexError: If no index in modeConfig.db.
        """
        if self.__modeConfig.select_current_index(
                index) != 0:  # 0 is APC_OK in eSPDI_def.h
            raise IndexError
        self.__mode_info = self.__update_mode_info()

    def __update_mode_info(self):
        return self.__modeConfig.get_current_mode_info()


class RectLogData:
    """This class is to save rectify log data.

    This class is to save rectify log data.
    Its attribute is follow the `eSPCtrl_RectLogData` in eSPDI_def.h.

    Args:
        dictionary: The dictonary of rectyLogData from eys3dPy.
        nRectifyLogIndex: The index user wanted to select.

    Raise:
        Exception: No rectify log.Please check rectify index.
    """
    @logger.catch
    def __init__(self, dictionary, nRectifyLogIndex):
        try:
            self.rectifyLogIndex = nRectifyLogIndex
            self.dictLog = self.__to_list(dictionary)
            for k, v in dictionary.items():
                setattr(self, k, v)
        except TypeError as e:
            raise Exception("No rectify log. Please check rectify index")

    def save_json(self, fname=None):
        """Save rectify log data as json file.

        To save rectify log data as json file.
        It save as `RectifyLog-{index}.json` to `EYS3D_HOME/logs` if fname is not provided.
        Default is `~/.eYs3D/logs/`.

        Args:
            fname (str): The filename for json file. Default is RectifyLog-{index}.json if fname is None. 
        """
        if fname is None:
            fname = "RectifyLog-{}.json".format(self.rectifyLogIndex)
        elif not fname.endswith(".json"):
            fname = "{}.json".format(fname)
        saved_file = os.path.join(get_EYS3D_HOME(), 'logs', fname)
        with open(saved_file, "w") as fp:
            json.dump(self.dictLog, fp, indent=4, sort_keys=True)
            logger.info("Save rectify log as json to {}".format(saved_file))

    def get_dict(self, ):
        """Get the dictionary of rectify log data.

        To get the dictionary of rectify log data.
        The key is refer to `eSPCtrl_RectLogData` in eSPDI_def.h.

        Returns:
            dict: The rectify log data as dictionary.
        """
        return self.dictLog

    def __to_list(self, dictLog):
        ret = dict({})
        for k, v in dictLog.items():
            if isinstance(v, np.ndarray):
                ret[k] = v.tolist()
            else:
                ret[k] = v
        return ret


#
