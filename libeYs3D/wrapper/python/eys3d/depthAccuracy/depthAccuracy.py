import eys3dPy
from eys3d import logger

class DepthAccuracy:
    """This class manage the functions related to DepthAccuracy.
    
    The design of this class follow the `DepthAccuracyOptions.cpp`.
    User could operate the function to get the accuracy information.

    Args:
        camera_device (obj): The camera_device is CameraDevice. 
    """
    def __init__(self, camera_device):
        self.__camera_device = camera_device
        self.__depthAccuracyOptions = self.__camera_device.get_depthAccuracyOptions(
        )

    def enable(self):
        """Enable depth accuracy function.
        
        To enable the depth accuracy function.

        Note:
            Notice that it would not guarantee the performance.
        """
        self.__depthAccuracyOptions.enable(True)
        self.__camera_device.set_depthAccuracyOptions(
            self.__depthAccuracyOptions)

    def disable(self):
        """Disable depth accuracy function.

        To disable the depth accuracy function.
        """
        self.__depthAccuracyOptions.enable(False)
        self.__camera_device.set_depthAccuracyOptions(
            self.__depthAccuracyOptions)

    def is_enabled(self):
        """To check the status.

        Check the accuracy status.

        Returns:
            bool: The return value. True for enable, False otherwise.
        """
        return self.__depthAccuracyOptions.is_enabled()

    @logger.catch
    def set_region_ratio(self, region_ratio):
        """Set the region ratio.

        [EYS3D][TODO][DOC]

        Args:
            region_ratio (float): The ratio of region to calculate.

        """
        if 0 < region_ratio <= 1.0:
            self.__depthAccuracyOptions.set_region_ratio(region_ratio)
            self.__camera_device.set_depthAccuracyOptions(
                self.__depthAccuracyOptions)
        else:
            raise ValueError("region_ratio is in 0 ~ 1.0 .")

    def get_region_ratio(self):
        """Get the region ratio.

        [EYS3D][TODO][DOC]

        Returns:
            float: The ratio of region that was set by user.
        """
        return self.__depthAccuracyOptions.get_region_ratio()

    def set_groundTruth_distance(self, ground_truth):
        """Set the ground truth distance to calculate.

        [EYS3D][TODO][DOC]
        The unit is millimeter.

        Args:
            ground_truth (int): The distance to the ground truth object in millimeter (mm).

        """
        self.__depthAccuracyOptions.set_groundTruth_distance(ground_truth)
        self.__camera_device.set_depthAccuracyOptions(
            self.__depthAccuracyOptions)

    def get_groundTruth_distance(self):
        """Get distance of the ground truth.

        [EYS3D][TODO][DOC]

        Returns:
            int: The ground truth distance that was set by user.
        """
        return self.__depthAccuracyOptions.get_groundTruth_distance()
