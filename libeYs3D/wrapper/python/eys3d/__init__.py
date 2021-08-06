import os
from loguru import logger

# Set environment variable before initialize eys3d system
cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "../../../..")  # The path of python_wrapper
os.environ['EYS3D_SDK_HOME'] = cfg_path

from eys3dPy import LIGHT_SOURCE_VALUE, COLOR_RAW_DATA_TYPE, DEPTH_RAW_DATA_TYPE, SENSORMODE_INFO, DEPTH_TRANSFER_CTRL, PIPELINE_RESULT, USB_PORT_TYPE, DECODE_TYPE
from .pipeline import Pipeline
from .frameset_pipeline import FrameSetPipeline
from .config import Config, ModeConfig
from .device import Device, EYS3DSystem
from .depthFilter import DepthFilterOptions
from .depthAccuracy import DepthAccuracy
from .cameraProperty import CameraProperty
from .utils import *

__all__ = [
    "Pipeline", "Config", "ModeConfig", "Device", "DepthFilterOptions",
    "DepthAccuracy", "CameraProperty", "FrameSetPipeline"
]

__version__ = "1.0.1"

# loguru config setting. The the max count of backup files is 100 and each file is not exceed than 10MB.
logger.add(os.path.join(get_EYS3D_HOME(), "logs", "python-eYs3d-{time}.log"),
           rotation="10MB",
           retention=100)
