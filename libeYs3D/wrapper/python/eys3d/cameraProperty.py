import eys3dPy


class CameraProperty:
    """This class contains the camera properties.

    This class contains the camera properties including auto exposure, auto white balance, 
    low light compesation, light source switch, and etc.
    User could controls the propeties by following function.
    [EYS3D][TODO][DOC]

    Args:
        camera_device (obj): CameraDevice.

    """
    def __init__(self, camera_device):
        self.__camera_device = camera_device

    def enable_AE(self, ):
        """Enable auto exposure mode.

        To enable auto exposure mode.
        """
        self.__camera_device.enable_AE()

    def disable_AE(self, ):
        """Disable auto exposure mode.

        To disable auto exposure mode.
        """
        self.__camera_device.disable_AE()

    def get_AE_status(self, ):
        """Get the status of auto exposure.

        To get the status of auto exposure.

        Returns:
            bool: The return value. True for enable, False otherwise.
        """
        return self.__camera_device.get_AE_status()

    def get_exposure_value(self, ):
        """Get the exposure value.

        To get the exposure value.
        The value is calculated by log2.
        The range of value is -13 ~ 3.

        Return:
            int: The exposure value. The range is -13 ~ 3.
        """
        return self.__camera_device.get_exposure_value()

    def set_exposure_value(self, value):
        """Set the exposure value.

        To set the exposure value.
        The range of value is -13 ~ 3.
        It would set to minimun or maximun value if input-value is out of range.

        Args:
            value (int): The exposure value. The range is -13 ~ 3.
        """
        val_range = self.get_exposure_range()
        if value >= val_range['Max']:
            value = val_range['Max']
        elif value <= val_range['Min']:
            value = val_range['Min']
        self.__camera_device.set_exposure_value(value)

    def get_manual_exposure_time(self, ):
        """Get the manual exposure time.

        To get the manual exposure time.
        [EYS3D][TODO][DOC]

        Returns:
            float: The exposure time. [EYS3D][TODO][DOC]
        """
        return self.__camera_device.get_manual_exposure_time()

    def set_manual_exposure_time(self, value):
        """Set the manual exposure time.

        To set the manual exposure time.
        [EYS3D][TODO][DOC]

        Args:
            value (float): The manual exposure time.
        """
        self.__camera_device.set_manual_exposure_time(value)

    def get_manual_global_gain(self, ):
        """Get the manual global gain.

        To get the manual global gain.
        [EYS3D][TODO][DOC]

        Returns:
            float: The exposure time. [EYS3D][TODO][DOC]
        """
        return self.__camera_device.get_manual_global_gain()

    def set_manual_global_gain(self, value):
        """Set the manual global gain.

        To set the manual global gain.
        [EYS3D][TODO][DOC]

        Args:
            value (float): The manual global gain.
        """
        self.__camera_device.set_manual_global_gain(value)

    def get_exposure_range(self):
        """Get the exposure range from eYs3D camera module.

        To get the exposure range as a dictionary.
        The key is following:
        * Max 
        * Min
        * Step
        * Default

        Returns:
            dict: The exposure range. The key is following:
                * Max 
                * Min
                * Step
                * Default
        """
        return self.__camera_device.get_exposure_range()

    def enable_AWB(self, ):
        """Enable auto white balance mode.

        To enable auto white balance mode.
        """
        self.__camera_device.enable_AWB()

    def disable_AWB(self, ):
        """Disable auto white balance mode.

        To disable auto white balance mode.
        """
        self.__camera_device.disable_AWB()

    def get_AWB_status(self, ):
        """Get the status of auto white balance.

        To get the status of auto white balance.

        Returns:
            bool: The return value. True for enable, False otherwise.

        """
        return self.__camera_device.get_AWB_status()

    def get_white_balance_temperature(self, ):
        """Get the white balance temperature.

        To get the white balance temperature.

        Returns:
            int: The white balance temperature (the range is 2800 ~ 6500).
        """
        return self.__camera_device.get_white_balance_temperature()

    def set_white_balance_temperature(self, value):
        """Set the white balance temperature.

        To set the white balance temperatue.
        The range is 2800 ~ 6500.

        Args:
            value: The white balance temperature.The range si 2800 ~ 6500.
        """
        range_temperature = self.__camera_device.get_white_balance_temperature_range(
        )
        if value not in range(range_temperature['Min'],
                              range_temperature['Max'] + 1):
            raise ValueError("Out of range.")
        self.__camera_device.set_white_balance_temperature(value)

    def get_white_balance_temperature_range(self):
        """Get the range of white balance temperature.
        
        To Get the range of white balance temperature as a dictionary.
        The key is following :
        * Max 
        * Min
        * Step
        * Default

        Returns:
            dict: The range of white balance temperature. The key is following:
                * Max 
                * Min
                * Step
                * Default

        """
        return self.__camera_device.get_white_balance_temperature_range()

    def get_low_light_compensation_status(self, ):
        """Get the status of low light compensation.

        To get the status of low light compensation.

        Returns:
            bool: The return value. True for enable, False otherwise.
        """
        return self.__camera_device.get_low_light_compensation_status()

    def enable_low_light_compensation(self):
        """Enable low light compesation mode.

        To enable low light compesation mode.
        """
        self.__camera_device.set_low_light_compensation(1)

    def disable_low_light_compensation(self):
        """Disable low light compesation mode.

        To disable low light compesation mode.
        """
        self.__camera_device.set_low_light_compensation(0)

    def get_light_source_status(self, ):
        """Get the status of light source.
        
        To get the status of light source.
        The options are 50 Hz and 60 Hz.

        Returns:
            LIGHT_SOURCE_VALUE: VALUE_50HZ is 50 Hz, VALUE_60HZ is 60 Hz.
        """
        return eys3dPy.LIGHT_SOURCE_VALUE(
            self.__camera_device.get_light_source_status())

    def set_light_source(self, value):
        """Set the light source.

        To set the light source
        The options are 50 Hz and 60 Hz.

        value (LIGHT_SOURCE_VALUE): Set to VALUE_50HZ for 50 Hz and VALUE_60HZ for 60 Hz
        """
        self.__camera_device.set_light_source(value)
