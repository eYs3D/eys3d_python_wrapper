from eys3d import logger


class IRProperty:
    """This class is to control the IR property.

    [TODO][EYS3D][DOC]

    args:
        camera_device(:obj): CameraDeivce.
    """
    def __init__(self, camera_device):
        self.__camera_device = camera_device
        self.__IRProperty = self.__camera_device.get_IR_property()

    def enable_extendIR(self, ):
        """Enable range extension of IR.

        To enable range extension of IR.
        The range is 0 ~ 15 after extend enabled.
        """
        self.__IRProperty.enable_extendIR(True)
        self.__camera_device.set_IR_property(self.__IRProperty)
        self.__update_IRProperty()

    def disable_extendIR(self, ):
        """Disable range extension of IR.

        To disable range extension of IR.
        The range is 0 ~ 6 after extend disabled.
        """
        self.__IRProperty.enable_extendIR(False)
        self.__camera_device.set_IR_property(self.__IRProperty)
        self.__update_IRProperty()

    def is_extendIR_enabled(self, ):
        """Get the status of IR range extension.

        To get the status of IR range extension.

        Returns:
            bool: The return value. True for enable, False otherwise.
        """
        return self.__IRProperty.is_extendIR_enabled()

    def get_IR_value(self):
        """Get the current value of IR.

        To get the current value of IR.

        Returns:
            int: The current value of IR.
        """
        return self.__IRProperty.get_IR_value()

    @logger.catch
    def set_IR_value(self, value):
        """Set the current value of IR.

        To set the current value of IR.

        Args:
            value: The IR value provided by user.
        """
        if not self.get_IR_min() <= value <= self.get_IR_max():
            raise ValueError("Out of range.")
        #self.__camera_device.set_IR_value(value)
        self.__IRProperty.set_IR_value(value)
        self.__camera_device.set_IR_property(self.__IRProperty)
        self.__update_IRProperty()

    def get_IR_max(self):
        """Get the max of IR value.

        To get the max of IR value.

        Returns:
            int: The max of IR value.
        """
        return self.__IRProperty.get_IR_max()

    def get_IR_min(self):
        """Get the min of IR value.

        To get the min of IR value.

        Returns:
            int: The min of IR value.
        """
        return self.__IRProperty.get_IR_min()

    def __update_IRProperty(self):
        self.__IRProperty = self.__camera_device.get_IR_property()
