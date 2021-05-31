class RegisterOptions:
    """Register options

    The class is to set the register options.
    It was designed to follow DMPreview/Register.

    User could enable periodic and save log.
    This class control FW, HW and sensor register.
    """
    def __init__(self, camera_device):
        self.__camera_device = camera_device
        self.__register_options = self.__camera_device.get_register_options()

    def enable_periodic_read(self, ):
        """Enable periodic read.

        To enable periodic read.
        """
        self.__register_options.enable_periodic_read(True)
        self.__camera_device.set_write_register_options(
            self.__register_options)

    def disable_periodic_read(self, ):
        """Disable periodic read.

        To disable periodic read.
        """
        self.__register_options.enable_periodic_read(False)
        self.__camera_device.set_write_register_options(
            self.__register_options)

    def is_periodic_read(self):
        """Check the status of periodic read.

        To check the status of periodic read.

        Returns:
             bool: The return value. True for enable, False otherwise.
        """
        return self.__register_options.is_periodic_read()

    def enable_saveLog(self):
        """Enable saving the register log.

        To enable saving the register log.

        The default saved directory is: libeYs3D/wrapper/python.
        User needs to export EYS3D_HOME before executing.
        """
        self.__register_options.enable_save_log(True)
        self.__camera_device.set_write_register_options(
            self.__register_options)

    def disable_saveLog(self):
        """Disable saving the register log.

        To disable saving the register log.
        """
        self.__register_options.enable_save_log(False)
        self.__camera_device.set_write_register_options(
            self.__register_options)

    def is_saveLog(self):
        """Check the status of save log.

        To check the status of save log.
        """
        return self.__register_options.is_save_log()

    def get_period_time(self):
        """Get the period time.

        To get the period time.
        The unit is microsecond.

        Returns:
            int: The period time. The unit is microsecond.
        """
        return self.__register_options.get_period_time()

    def set_period_time(self, timeMs):
        """Set the period time.

        To set the period time.
        """
        self.__register_options.set_period_time(timeMs)
        self.__camera_device.set_write_register_options(
            self.__register_options)

    def get_FW_register(self, addr):
        """Get the value from firmware register.

        To get the value from firmware register.

        Args:
            addr (:int): The register address. It is available for integer or heximal.

        Returns:
            int: The value from firmware register address.
        """
        return self.__camera_device.get_FW_register(addr)

    def set_FW_register(self, addr, value):
        """Set the value to firmware register.

        To set the value to firmware register.

        Args:
            addr (:int): The register address. It is available for integer or heximal.
            value (:int): The value for register. It is available for integer or heximal. 
        """
        self.__camera_device.set_FW_register(addr, value)

    def get_HW_register(self, addr):
        """Get the value from ASIC register.

        To get the value from ASIC register.

        Args:
            addr (:int): The register address. It is available for integer or heximal.

        Returns:
            int: The value from ASIC register address.
        """
        return self.__camera_device.get_HW_register(addr)

    def set_HW_register(self, addr, value):
        """Set the value to ASIC register.

        To set the value to ASIC register.

        Args:
            addr (:int): The register address. It is available for integer or heximal.
            value (:int): The value for register. It is available for interg or heximal. 
        """
        self.__camera_device.set_HW_register(addr, value)

    def get_sensor_register(self, addr, sensor_mode, slave_id):
        """Get the value from I2C register.

        To get the value from I2C register.

        Args:
            addr (:int): The register address. It is available for integer or heximal.
            sensor_mode (:SENSORMODE_INFO): The index to select. Please refer SENSORMODE_INFO.
            slave_id (:int): [TODO][EYS3D][DOC]

        Returns:
            int: The value from I2C register address.
        """
        return self.__camera_device.get_sensor_register(
            addr, sensor_mode, slave_id)

    def set_sensor_register(self, addr, value, sensor_mode, slave_id):
        """Set the value to ASIC register.

        To set the value to ASIC register.

        Args:
            addr (:int): The register address. It is available for integer or heximal.
            value (:int): The value for register. It is available for interg or heximal. 
            sensor_mode (:SENSORMODE_INFO): The index to select. Please refer SENSORMODE_INFO.
            slave_id (:int): [TODO][EYS3D][DOC]
        """
        self.__camera_device.set_sensor_register(addr, value, sensor_mode,
                                                 slave_id)
