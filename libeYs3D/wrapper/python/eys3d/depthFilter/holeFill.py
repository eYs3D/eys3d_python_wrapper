from eys3d import logger 

class HoleFill:
    """Performe HoleFill.

    This function tries to fill the holes in the depth image. Users can strengthen the
    effect by increasing the parameter “level”. The parameter “horizontal” controls
    the hole filtering to be performed horizontally or vertically.

    Args:
        camera_device (obj): CameraDevice.
        depthFilterOptions (obj): DepthFilterOptions.

    """
    def __init__(self, camera_device, depthFilterOptions):
        self.__camera_device = camera_device
        self.__depthFilterOptions = depthFilterOptions

    #@__setDepthFilterOptions
    def enable(self):
        """Enable holeFill.

        To enable holeFill.
        """
        self.__depthFilterOptions.enable_holeFill(True)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    #@__setDepthFilterOptions
    def disable(self):
        """Disable holeFill.

        To disable holeFill.
        """
        self.__depthFilterOptions.enable_holeFill(False)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def is_enabled(self):
        """Check the status.

        To check the status of subsample function.

        Returns:
            bool: True for enable. False otherwise.
        """
        return self.__depthFilterOptions.is_holeFill_enabled()

    #@__setDepthFilterOptions
    def set_kernel_size(self, size=1):
        """Set the kernel size.

        To set the kernel size for hole filtering.
        
        Args:
            size (int): The kernel size for hole filtering. Defalut is 1.
        """
        self.__depthFilterOptions.set_kernel_size(size)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get_kernel_size(self, ):
        """Get the kernel size.

        To get the kernel size user provided.

        Returns:
            int: The kernel size for hole filtering.
        """
        return self.__depthFilterOptions.get_kernel_size()

    #@__setDepthFilterOptions
    @logger.catch
    def set_level(self, level):
        """Set the level.

        To set the level for hole filling.
        
        Args:
            level (int): The level for hole filling. The larger one means heavier effect. The range is 1 ~ 3.

        """
        if not 1 <= level <= 3:
            raise ValueError("Out of range.")
        self.__depthFilterOptions.set_level(level)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get_level(self):
        """Get the level.

        To get the level for hole filling.

        Returns:
            int: The level for hole filling.
        """
        return self.__depthFilterOptions.get_level()

    #@__setDepthFilterOptions
    def enable_horizontal(self, ):
        """Enable horizontal.

        To enable horizontal hole filiing.

        """
        self.__depthFilterOptions.set_horizontal(True)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def disable_horizontal(self, ):
        """Disable horizontal.

        To disable horizontal hole filiing.

        """
        self.__depthFilterOptions.set_horizontal(False)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def is_horizontal(self):
        """Check the status of horizontal.

        To check the status of horizontal.

        Returns:
            bool: True for enable. False otherwise.

        """
        return self.__depthFilterOptions.is_horizontal()

    def set(self, kernel_size, level):
        """Set the config of the hole filling.

        To set the total argument about hole filling.

        Args:
            size (int): The kernel size for hole filtering. Defalut is 1.
            level (int): The level for hole filling. The larger one means heavier effect.

        """
        if kernel_size:
            self.__depthFilterOptions.set_kernel_size(kernel_size)
        if level:
            self.__depthFilterOptions.set_level(level)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def get(self, ):
        """Get the config of the hole filiing to a dictionary.

        To get the total argument about hole filling.
        It return a dictionary.

        Returns:
            dict: The dictionary with following keys:
            kernel_size (int): The kernel size for hole filtering. Defalut is 1.
            level (int): The level for hole filling. The larger one means heavier effect.

        """
        kernel_size = self.__depthFilterOptions.get_kernel_size()
        level = self.__depthFilterOptions.get_level()
        return {
            'kernel_size': kernel_size,
            'level': level,
        }
