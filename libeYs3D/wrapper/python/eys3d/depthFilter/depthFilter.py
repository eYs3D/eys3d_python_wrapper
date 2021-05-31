import eys3dPy
from eys3d import logger
from .holeFill import HoleFill
from .edgePreServingFilter import EdgePreServingFilter
from .subsample import Subsample
from .temporalFilter import TemporalFilter
from .removeCurve import RemoveCurve


class DepthFilterOptions:
    """Filter type apply to the depthfilter.

    It includes: subsample, edgePreServingFilter, holeFill, temporalFilter and
    removeCurve sub function.
    Please see each sub function comment for detail usage.

    Args:
        camera_device (obj): CameraDevice.
    """
    @logger.catch
    def __init__(self, camera_device):
        try:
            self.__camera_device = camera_device
            self.__depthFilterOptions = self.__camera_device.get_depthFilterOptions(
            )

            self.subsample = Subsample(self.__camera_device,
                                       self.__depthFilterOptions)
            self.edgePreServingFilter = EdgePreServingFilter(
                self.__camera_device, self.__depthFilterOptions)
            self.holeFill = HoleFill(self.__camera_device,
                                     self.__depthFilterOptions)
            self.temporalFilter = TemporalFilter(self.__camera_device,
                                                 self.__depthFilterOptions)
            self.removeCurve = RemoveCurve(self.__camera_device,
                                           self.__depthFilterOptions)
        except:
            raise ImportError

    def enable(self):
        """Enable DepthFilter function.

        To enable DepthFilter function.
        """
        self.__depthFilterOptions.enable(True)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def disable(self):
        """Disable DepthFilter function.

        To disable DepthFilter function.
        """
        self.__depthFilterOptions.enable(False)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def is_enabled(self):
        """Check the depthFilter status.

        To check the status of depth filtering function.

        Returns:
            bool: True for enable. False otherwise.
        """
        return self.__depthFilterOptions.is_enabled()

    def get_bytes_per_pixel(self):
        """Get the number of bytes per pixel.

        To get the number of bytes for one pixel.

        Returns:
            int: The number of bytes for saving one pixel.
        """
        return self.__depthFilterOptions.get_bytes_per_pixel()
