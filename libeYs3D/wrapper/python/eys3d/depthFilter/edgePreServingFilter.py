from eys3d import logger

# EdgepreserveFilter
class EdgePreServingFilter:
    """Perform edge preserve filtering.

    This function can smooth the depth image but still reserve the edge
    information. User can strengthen the effect by increasing the parameter
    “level”.
    """
    def __init__(self, camera_device, depthFilterOptions):
        self.__camera_device = camera_device
        self.__depthFilterOptions = depthFilterOptions

    def enable(self):
        """Enable edge preserve filtering.

        To enable edge preserve filtering.
        """
        self.__depthFilterOptions.enable_edgePreServingFilter(True)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def disable(self):
        """Disable edge preserve filtering.

        To disable edge preserve filtering.
        """
        self.__depthFilterOptions.enable_edgePreServingFilter(False)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def is_enabled(self):
        """Check the status.

        To check the status of edge preserve filtering function.

        Returns:
            bool: True for enable. False otherwise.
        """
        return self.__depthFilterOptions.is_edgePreServingFilter_enabled()

    @logger.catch
    def set_edge_level(self, level):
        """Set the level of edge.

        To set the level for edge preserve filtering.

        Args:
            level (int): The level for edge preserve filtering (larger means heavier effect). The range is 1 ~ 10.
        """
        if not 1 <= level <= 10:
            raise ValueError("Out of range.")
        self.__depthFilterOptions.set_edge_level(level)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get_edge_level(self, ):
        """Get the level.

        To get the level of the edge preserve filtering.

        Returns:
            int: The level for edge preserve filtering.
        """
        return self.__depthFilterOptions.get_edge_level()

    # The sigma is fixed.
    # def set_sigma(self, sigma=0.015):
    #     """Set the sigma.

    #     To set the sigma that is the internal parameter for edge preserve filtering.

    #     Args:
    #         sigma (float): The internal parameter for edge preserve filtering. Default is 0.015.
    #     """
    #     self.__depthFilterOptions.set_sigma(sigma)
    #     self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get_sigma(self, ):
        """Get the sigma.

        To get the sigma value.
        This value is fixed.

        Returns:
            float: The internal parameter for edge preserve filtering.
        """
        return round(self.__depthFilterOptions.get_sigma(), 3)

    # The lambda is fixed.
    # def set_lambda(self, Lambda=0.1):
    #     """Set the lambda.

    #     To set the lambda.
    #     It is a internal parameter for edge preserve filtering.

    #     Args:
    #         Lambda (float): The internal parameter for edge preserve filtering. Default is 0.1 .
    #     """
    #     self.__depthFilterOptions.set_lambda(Lambda)
    #     self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get_lambda(self, ):
        """Get the lambda.

        To get the lambda user provided.
        This value is fixed.

        float: The internal parameter for edge preserve filtering.

        """
        return round(self.__depthFilterOptions.get_lambda(), 1)

    def set(self, edge_level):
        """Set the config fo the edge preserving filtering.

        To set all the argument about edge preserve filtering.

        Args:
            level (int): The level for edge preserve filtering (larger means heavier effect).

        """
        if edge_level:
            self.set_edge_level(edge_level)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get(self):
        """Get the config of the edge preserve filtering to a dictionary.

        To get all the argument about edge preserve filtering.
        It returns a dictionary.

        Returns:
            dict: The dictionary with following keys:

            level (int): The level for edge preserve filtering (larger means heavier effect).
            sigma (str): The internal parameter for edge preserve filtering. Default is 0.015.
            Lambda (str): The internal parameter for edge preserve filtering. Default is 0.1 .

        """
        level = self.get_edge_level()
        sigma = self.get_sigma()
        Lambda = self.get_lambda()
        return dict({'level': level, 'sigma': sigma, 'lambda': Lambda})
