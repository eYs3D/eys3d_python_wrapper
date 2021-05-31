# Subsample
from eys3d import logger
class Subsample:
    """Perform subsampling process.

    This function mainly scales the depth image down to reduce the computational loading.
    It provides users two kinds of filtering methods (median and mean filtering) to subsample the depth image. 
    Furthermore, this function should be used with “EtronDI_ApplyFilters”. 
    Then, you have to call “EtronDI_ApplyFilters” before finishing the process of depth filtering, if you have
    called this function at the beginning of the process of depth filtering.

    Args:
        camera_device (obj): CameraDevice.
        depthFilterOptions (obj): DepthFilterOptions.
    """
    def __init__(self, camera_device, depthFilterOptions):
        self.__camera_device = camera_device
        self.__depthFilterOptions = depthFilterOptions

    #@__setDepthFilterOptions
    def enable(self):
        """Enable subsample.

        To enable subsample.
        """
        self.__depthFilterOptions.enable_subsample(True)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    #@__setDepthFilterOptions
    def disable(self):
        """ Disable subsample.

        To disable subsample.
        """
        self.__depthFilterOptions.enable_subsample(False)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def is_enabled(self):
        """Check the status.

        To check the status of subsample function.

        Returns:
            bool: True for enable. False otherwise.
        """
        return self.__depthFilterOptions.is_subsample_enabled()
    
    @logger.catch
    def set(self, mode_index):
        """Set the filtering mode and scaling factor.

        To set the filtering mode and scaling factor.

        Args:
            mode_index (int): The mode for subsample. 
                0: median filter and factor 2.
                1: median filter and factor 3.
                2: mean filter and factor 4.
                3: mean filter and factor 5.
        
        """
        if mode_index not in range(4):
            raise ValueError("Out of range.")
        if mode_index == 0:
            self.__depthFilterOptions.set_subsample_mode(0)
            self.__depthFilterOptions.set_subsample_factor(2)
        elif mode_index == 1:
            self.__depthFilterOptions.set_subsample_mode(0)
            self.__depthFilterOptions.set_subsample_factor(3)
        elif mode_index == 2:
            self.__depthFilterOptions.set_subsample_mode(1)
            self.__depthFilterOptions.set_subsample_factor(4)
        elif mode_index == 3:
            self.__depthFilterOptions.set_subsample_mode(1)
            self.__depthFilterOptions.set_subsample_factor(5)

        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get(self, ):
        """Get the filtering mode and scaling factor to a dictionary.

        To get the filtering mode and scaling factor.
        It return a dictionary.

        Returns:
            dict: The dictionary with following keys:
            
            mode_index (int): The filtering mode. 0: median filter. 1: mean filter.
            factor (int): The scaling factor.
        """
        mode_index = self.__depthFilterOptions.get_subsample_mode()
        factor = self.__depthFilterOptions.get_subsample_factor()

        return dict({'mode_index': mode_index, 'factor': factor})
