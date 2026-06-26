import os
import numpy as np
import json
from typing import Dict, Tuple, Optional, Any

import eys3dPy
from eys3d import logger, COLOR_RAW_DATA_TYPE, DEPTH_TRANSFER_CTRL, DEPTH_RAW_DATA_TYPE, USB_PORT_TYPE
from .utils import get_EYS3D_HOME


class Config:
    """Stream configuration for eYs3D cameras.

    Configures color/depth stream resolution, format, FPS, and depth data type.
    Use set_preset_mode_config() for easy setup from ModeConfig.db, or manually
    configure with set_color_stream() and set_depth_stream().

    Attributes:
        colorStreamFormat: Color format (YUY2 or MJPG).
        depthStreamFormat: Depth transfer control (colorful, gray, or raw).
        depthDataType: Depth bit format (8/11/14 bits, ILM variants).
        ep0Width/ep0Height: Color resolution.
        ep1Width/ep1Height: Depth resolution.
        ep0fps/ep1fps: Frame rates for color/depth.
        interleavefps: Interleave mode FPS (0 = disabled).
        rectify: Whether rectification is enabled.
    """
    def __init__(self) -> None:

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
        self.rectifyFileIndex = 0

    def set_color_stream(
        self,
        streamFormat: COLOR_RAW_DATA_TYPE,
        nEP0Width: int,
        nEP0Height: int,
        fps: int
    ) -> None:
        """Configure color stream format and resolution.

        Args:
            streamFormat: Color format - use COLOR_RAW_DATA_TYPE enum:
                - COLOR_RAW_DATA_YUY2 (0): YUY2 format
                - COLOR_RAW_DATA_MJPG (1): MJPG compressed format
            nEP0Width: Color stream width in pixels.
            nEP0Height: Color stream height in pixels.
            fps: Target frame rate.

        Note:
            Refer to camera module PIF or ModeConfig.db for supported resolutions.
        """
        self.colorStreamFormat = streamFormat
        self.ep0Width = nEP0Width
        self.ep0Height = nEP0Height
        self.ep0fps = fps

    def set_depth_stream(
        self,
        streamFormat: DEPTH_TRANSFER_CTRL,
        nEP1Width: int,
        nEP1Height: int,
        fps: int
    ) -> None:
        """Configure depth stream format and resolution.

        Args:
            streamFormat: Depth transfer control - use DEPTH_TRANSFER_CTRL enum:
                - DEPTH_IMG_NON_TRANSFER (0): Raw depth data, no colorization
                - DEPTH_IMG_GRAY_TRANSFER (1): Grayscale depth visualization
                - DEPTH_IMG_COLORFUL_TRANSFER (2): Colorful depth heatmap (default)
            nEP1Width: Depth stream width in pixels.
            nEP1Height: Depth stream height in pixels.
            fps: Target frame rate.

        Note:
            Refer to camera module PIF or ModeConfig.db for supported resolutions.
        """
        self.depthStreamFormat = streamFormat
        self.ep1Width = nEP1Width
        self.ep1Height = nEP1Height
        self.ep1fps = fps

    def set_depth_data_type(self, depth_data_type: int) -> None:
        """Set the depth data bit precision.

        Configures depth data type (bit depth) for non-G120 cameras.
        For G120 (eSP936 series chip), depth type is handled automatically in set_preset_mode_config().

        Args:
            depth_data_type: Depth precision in bits. Valid values:
                - 8: 8-bit depth (lower precision, smaller data)
                - 11: 11-bit depth (standard precision)
                - 14: 14-bit depth (high precision)

        Raises:
            Exception: If depth_data_type is not 0, 8, 11, or 14.

        Note:
            Available bit depths depend on camera module. Refer to PIF documentation.
            G120 cameras ignore this call - use depth_bits param in set_preset_mode_config().
        """
        if depth_data_type not in (0, 8, 11, 14):
            raise Exception(
                "depth_data_type is out of range. Please refer document")

        is_G120 = (self.pid == 0x0202 or self.pid == 0x0211)
        if is_G120:
            # G120 (eSP936) handles depth configuration in __update_config
            return

        if self.mode_info.videoModeD11OrColorOnly != 0xff or self.mode_info.videoModeZ14 != 0xff:
            self.depthDataType = DEPTH_RAW_DATA_TYPE(self.mode_info.videoModeZ14) if depth_data_type == 14 \
                else DEPTH_RAW_DATA_TYPE(self.mode_info.videoModeD11OrColorOnly)
        else:
            self.depthDataType = self.__DepthDataToFormatType(depth_data_type)

    def set_depth_data_type_with_advanced_setting(
        self,
        depth_data_type: int,
        is_rectify: bool,
        is_interleave_mode: bool
    ) -> None:
        """Configure depth type with rectification and interleave mode.

        Manually configure depth data type along with rectification and interleave mode.
        The final DEPTH_RAW_DATA_TYPE enum value depends on all three parameters.

        Args:
            depth_data_type: Depth precision in bits (8, 11, or 14).
            is_rectify: Enable rectified depth output (lens distortion corrected).
            is_interleave_mode: Enable interleave mode (color/depth alternating frames).

        Note:
            Interleave mode (ILM) is required for G120 eSP936 series chip cameras.
            When ILM is enabled, color and depth frames alternate on a single endpoint.
        """
        if is_rectify:
            self.enable_rectify()
        else:
            self.disable_rectify()
        if is_interleave_mode:
            self.interleavefps = self.ep0fps if self.ep0fps else self.ep1fps
        self.set_depth_data_type(depth_data_type)

    def set_fps(self, fps: int) -> None:
        """Override frame rate for both color and depth streams.

        Args:
            fps: Target frame rate for both streams.
        """
        self.ep1fps = self.ep0fps = fps

    def get_config(self) -> Dict[str, Any]:
        """Get the current stream configuration as a dictionary.

        Returns:
            Dictionary containing:
                - colorFormat: COLOR_RAW_DATA_TYPE (YUY2/MJPG)
                - colorWidth: Color stream width in pixels
                - colorHeight: Color stream height in pixels
                - depthStreamFormat: DEPTH_TRANSFER_CTRL (colorful/gray/raw)
                - depthWidth: Depth stream width in pixels
                - depthHeight: Depth stream height in pixels
                - actualFps: Configured frame rate
                - depthFormat: DEPTH_RAW_DATA_TYPE enum value
                - ILM: Interleave mode FPS (0 = disabled)
                - rectify: Whether rectification is enabled
                - rectifyFileIndex: Rectification calibration file index
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
            "rectifyFileIndex": self.rectifyFileIndex,
        })

        return conf

    def get_color_stream_resolution(self) -> Tuple[int, int]:
        """Get color stream resolution as (height, width).

        Returns:
            Tuple of (height, width) in pixels. Note: height comes first
            to match numpy array shape convention (rows, cols).
        """
        return (self.ep0Height, self.ep0Width)

    def get_depth_stream_resolution(self) -> Tuple[int, int]:
        """Get depth stream resolution as (height, width).

        Returns:
            Tuple of (height, width) in pixels. Note: height comes first
            to match numpy array shape convention (rows, cols).
        """
        return (self.ep1Height, self.ep1Width)

    def set_preset_mode_config(
        self,
        pid: int,
        index: int,
        usb_type: int,
        depth_bits: Optional[int] = None,
    ) -> None:
        """Load configuration from ModeConfig.db preset.

        Simplifies configuration by loading settings from the mode database.
        The database contains pre-defined resolutions, formats, and FPS for each mode.

        Args:
            pid: Product ID of camera module (e.g., 0x0202 for G120C, 0x0211 for G120IR).
                Supports both integer (514) and hexadecimal (0x0202) formats.
            index: Mode index from ModeConfig.db (typically 0-19).
            usb_type: USB port type - 2 for USB2.0, 3 for USB3.0.
            depth_bits: Depth precision override for G120 cameras only (11 or 14).
                If None, uses default from database. Ignored for non-G120 cameras.

        Example:
            >>> conf = Config()
            >>> conf.set_preset_mode_config(0x0202, 1, 3, depth_bits=14)  # G120 Mode 1, 14-bit
        """
        modeConfig = ModeConfig(pid, index, usb_type)
        mode_info = modeConfig.get_current_mode_info()
        self.__update_config(mode_info, pid, depth_bits)

    def enable_rectify(self):
        self.rectify = True

    def disable_rectify(self):
        self.rectify = False

    def __update_config(self, mode_info, pid, depth_bits=None):
        self.pid = pid

        # Common settings for all cameras (must be set before depthDataType calculation)
        self.mode_info = mode_info
        self.interleavefps = mode_info.iInterLeaveModeFPS
        self.rectifyFileIndex = mode_info.rectifyFileIndex

        # Set rectify BEFORE depthDataType calculation (used by __DepthDataToFormatType)
        if mode_info.bRectifyMode:
            self.enable_rectify()
        else:
            self.disable_rectify()

        # Check if this is G120 camera (PIDs: 0x0202 or 0x0211)
        is_G120 = (pid == 0x0202 or pid == 0x0211)
        if is_G120:
            # For G120, use K_Resolution for color and T_Resolution for depth
            # Color format from eDecodeType_K
            self.colorStreamFormat = COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2 if mode_info.eDecodeType_K == 0 else COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_MJPG

            # Check if depth-only mode (Mode_Description == "D")
            is_depth_only = (mode_info.csModeDesc == "D")
            is_color_only = mode_info.T_Resolution.Width == 0 or mode_info.T_Resolution.Height == 0

            if is_depth_only:
                self.ep0Height = 0
                self.ep0Width = 0
            else:
                self.ep0Height = mode_info.K_Resolution.Height
                self.ep0Width = mode_info.K_Resolution.Width

            # Depth resolution from T_Resolution
            self.ep1Height = mode_info.T_Resolution.Height
            self.ep1Width = mode_info.T_Resolution.Width

            # FPS: prefer color fps, fallback to depth fps
            self.ep0fps = 0 if not mode_info.vecColorFps else mode_info.vecColorFps[0]
            self.ep1fps = 0 if not mode_info.vecDepthFps else mode_info.vecDepthFps[0]

            # G120 depthDataType: use videoModeD11OrColorOnly for 11-bit, videoModeZ14 for 14-bit
            if is_color_only:
                self.depthDataType = DEPTH_RAW_DATA_TYPE(mode_info.videoModeD11OrColorOnly) if mode_info.videoModeD11OrColorOnly else DEPTH_RAW_DATA_TYPE(0)
            else:
                # Use passed depth_bits if provided, otherwise use default from database
                default_depth_bits = mode_info.vecDepthType[0] if mode_info.vecDepthType else 11
                actual_depth_bits = depth_bits if depth_bits else default_depth_bits
                if actual_depth_bits == 11:
                    self.depthDataType = DEPTH_RAW_DATA_TYPE(mode_info.videoModeD11OrColorOnly)
                elif actual_depth_bits == 14:
                    self.depthDataType = DEPTH_RAW_DATA_TYPE(mode_info.videoModeZ14)
                else:
                    # Fallback for unsupported depth bits (e.g., 8-bit not supported on G120)
                    self.depthDataType = DEPTH_RAW_DATA_TYPE(mode_info.videoModeD11OrColorOnly)

        else:
            # Traditional cameras: use L_Resolution and D_Resolution
            self.colorStreamFormat = COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_YUY2 if mode_info.eDecodeType_L == 0 else COLOR_RAW_DATA_TYPE.COLOR_RAW_DATA_MJPG
            self.ep0Height = mode_info.L_Resolution.Height
            self.ep0Width = mode_info.L_Resolution.Width
            self.ep1Height = mode_info.D_Resolution.Height
            self.ep1Width = mode_info.D_Resolution.Width
            self.ep0fps = 0 if not mode_info.vecColorFps else mode_info.vecColorFps[0]
            self.ep1fps = 0 if not mode_info.vecDepthFps else mode_info.vecDepthFps[0]

            # Traditional depthDataType logic (self.rectify is already set above)
            self.depthDataType = DEPTH_RAW_DATA_TYPE(mode_info.videoModeD11OrColorOnly) \
                if (mode_info.videoModeD11OrColorOnly != 0xff) \
                else self.__DepthDataToFormatType(mode_info.vecDepthType[0] if len(mode_info.vecDepthType) != 0 else 0)

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
        if (self.pid == 0x204 and 400 == self.ep1Height) or (self.pid == 0x173 and 460 == self.ep1Height) or (self.pid == 0x180 and 460 == self.ep1Height):
            # This block for Hypatia2 scale down mode
            depth_data_bit = int(depth_data_bit) + DEPTH_RAW_DATA_SCALE_DOWN_MODE_OFFSET
            depth_data_bit = eys3dPy.DEPTH_RAW_DATA_TYPE(depth_data_bit)
        if self.interleavefps == (self.ep0fps if self.ep0fps else self.ep1fps):  # ILM
            depth_data_bit = int(depth_data_bit) + DEPTH_RAW_DATA_INTERLEAVE_MODE_OFFSET
            depth_data_bit = DEPTH_RAW_DATA_TYPE(depth_data_bit)

        return depth_data_bit


class ModeConfig:
    """Interface to ModeConfig.db camera configuration database.

    Provides access to pre-defined camera modes stored in ModeConfig.db.
    Each mode specifies resolution, format, FPS, and feature support.

    Args:
        pid: Product ID of camera module (e.g., 0x0202 for G120C).
        index: Initial mode index to select (0-based).
        usb_type: USB port type - 2 for USB2.0, 3 for USB3.0.

    Raises:
        Exception: If pid is not found in database.
    """
    def __init__(self, pid: int, index: int, usb_type: int) -> None:
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

    def get_current_index(self) -> int:
        """Get the currently selected mode index.

        Returns:
            Mode index (0-based).
        """
        current_index = self.__modeConfig.get_current_index()
        self.__index = current_index
        return self.__index

    def get_current_mode_info(self) -> eys3dPy.MODE_CONFIG:
        """Get MODE_CONFIG object for the current mode.

        Returns:
            MODE_CONFIG object with attributes:
                - iMode: Mode number
                - iUSB_Type: USB port type
                - iInterLeaveModeFPS: ILM FPS (0 = disabled)
                - eDecodeType_L: Color decode type (L_Resolution)
                - eDecodeType_K: Color decode type (K_Resolution, G120)
                - eDecodeType_T: Depth decode type (T_Resolution, G120)
                - L_Resolution: Color resolution (traditional cameras)
                - D_Resolution: Depth resolution (traditional cameras)
                - K_Resolution: Color resolution (G120 eSP936 series chip)
                - T_Resolution: Depth resolution (G120 eSP936 series chip)
                - vecDepthType: Supported depth bit types [8, 11, 14]
                - vecColorFps: Supported color frame rates
                - vecDepthFps: Supported depth frame rates
                - bRectifyMode: Whether rectification is enabled
                - rectifyFileIndex: Rectification calibration file index
                - videoModeD11OrColorOnly: Video mode value for 11-bit/color-only
                - videoModeZ14: Video mode value for 14-bit depth
                - csModeDesc: Mode description string ("C+D", "D", etc.)
        """
        return self.__mode_info

    def get_mode_count(self) -> int:
        """Get total number of available modes for this camera.

        Returns:
            Number of modes in ModeConfig.db for the current PID.
        """
        return self.__maxIndex

    def get_modes(self) -> None:
        """Get all modes. Not implemented.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError

    @logger.catch()
    def select_current_index(self, index: int) -> None:
        """Select a different mode by index.

        Args:
            index: Mode index to select (0-based).

        Raises:
            IndexError: If index is out of range for this camera.
        """
        if self.__modeConfig.select_current_index(
                index) != 0:  # 0 is APC_OK in eSPDI_def.h
            raise IndexError
        self.__mode_info = self.__update_mode_info()

    def __update_mode_info(self):
        return self.__modeConfig.get_current_mode_info()


class RectLogData:
    """Rectification calibration log data container.

    Wraps the eSPCtrl_RectLogData structure from the SDK.
    Contains camera intrinsic/extrinsic parameters for stereo rectification.

    Args:
        dictionary: Dictionary of rectifyLogData from eys3dPy C++ binding.
        nRectifyLogIndex: Rectification file index (typically 0-2).

    Raises:
        Exception: If rectify log is not available for the given index.

    Attributes:
        rectifyLogIndex: The index used to retrieve this data.
        dictLog: Dictionary form with numpy arrays converted to lists.
    """
    @logger.catch
    def __init__(self, dictionary: Dict[str, Any], nRectifyLogIndex: int) -> None:
        try:
            self.rectifyLogIndex = nRectifyLogIndex
            self.dictLog = self.__to_list(dictionary)
            for k, v in dictionary.items():
                setattr(self, k, v)
        except TypeError as e:
            raise Exception("No rectify log. Please check rectify index")

    def save_json(self, fname: Optional[str] = None) -> None:
        """Save rectification log data to JSON file.

        Saves calibration data to $EYS3D_HOME/logs/ (default: ~/.eYs3D/logs/).

        Args:
            fname: Output filename. If None, uses "RectifyLog-{index}.json".
                If provided without .json extension, it will be added.
        """
        if fname is None:
            fname = "RectifyLog-{}.json".format(self.rectifyLogIndex)
        elif not fname.endswith(".json"):
            fname = "{}.json".format(fname)
        saved_file = os.path.join(get_EYS3D_HOME(), 'logs', fname)
        with open(saved_file, "w") as fp:
            json.dump(self.dictLog, fp, indent=4, sort_keys=True)
            logger.info("Save rectify log as json to {}".format(saved_file))

    def get_dict(self) -> Dict[str, Any]:
        """Get rectification data as a JSON-serializable dictionary.

        All numpy arrays are converted to Python lists for JSON compatibility.
        Keys correspond to eSPCtrl_RectLogData fields in eSPDI_def.h.

        Returns:
            Dictionary containing calibration parameters (intrinsics, extrinsics).
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
