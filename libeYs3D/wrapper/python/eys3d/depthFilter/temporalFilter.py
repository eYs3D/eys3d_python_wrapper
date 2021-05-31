from eys3d import logger

class TemporalFilter:
    """Perform temporal filter.

    This function can reduce the variation of each depth pixel by mixing the current
    depth image and the previous ones. Users can control the mixing ratio through
    the parameter “alpha”. Increasing it can strengthen the influence of the current
    depth image.

    Args:
        camera_device (obj): CameraDevice.
        depthFilterOptions (obj): DepthFilterOptions.
    """
    def __init__(self, camera_device, depthFilterOptions):
        self.__camera_device = camera_device
        self.__depthFilterOptions = depthFilterOptions

    def enable(self, ):
        """Enable temporal filter.

        To enable temporal filter.
        """
        self.__depthFilterOptions.enable_temporalFilter(True)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def disable(self, ):
        """Disable temporal filter.

        To disable temporal filter.
        """
        self.__depthFilterOptions.enable_temporalFilter(False)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def is_enabled(self, ):
        """Check the status.

        To check the status of temporal filtering function.

        Returns:
            bool: True for enable. False otherwise.
        """
        return self.__depthFilterOptions.is_temporalFilter_enabled()

    @logger.catch
    def set_alpha(self, alpha):
        """Set the alpha.

        To set the alpha the user could control the mixing raio.

        Args:
            alpha (float): The weighting ratio for controlling the mix of the current depthimage and the passing depth images. The range is 0 ~ 1.0.

        """
        if not 0 < alpha < 1.0:
            raise ValueError("Out of range.")
        self.__depthFilterOptions.set_alpha(alpha)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get_alpha(self, ):
        """Get the alpha.

        To get the alpha user provided.

        Returns:
            float: The alpha value.
        """
        return round(self.__depthFilterOptions.get_alpha(), 3)

    @logger.catch
    def set_history(self, history):
        """Set the history

        To set the history value which is the number of passing depth images to be recorded.

        Args:
            history (int): Number of passing depth images to be recorded.The range is 2 ~ 3.
        """
        if not 2 <= history <= 3:
            raise ValueError("Out of range.")
        self.__depthFilterOptions.set_history(history)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get_history(self, ):
        """Get the history.

        To get the history.

        Returns:
            int: The number of passing depth images to be recorded.
        """
        return self.__depthFilterOptions.get_history()

    def set(self, alpha, history):
        """Set the config fo the temporal filtering.

        To set all the argument about temporal filtering.

        Args:
            alpha (float): The weighting ratio for controlling the mix of the current depthimage and the passing depth images.
            history (int): Number of passing depth images to be recorded.
        """
        if alpha:
            self.__depthFilterOptions.set_alpha(alpha)
        if history:
            self.__depthFilterOptions.set_history(history)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get(self):
        """Get the config of the temporal filtering to a dictionary.

        To get all the total argument about temporal filtering.
        It returns a dictionary.

        Returns:
            dict: The dictionary with following keys:

            alpha (str): The weighting ratio for controlling the mix of the current depthimage and the passing depth images.
            history (int): Number of passing depth images to be recorded.

        """
        alpha = self.__depthFilterOptions.get_alpha()
        history = self.__depthFilterOptions.get_history()
        return dict({'alpha': round(alpha, 1), 'history': round(history)})
