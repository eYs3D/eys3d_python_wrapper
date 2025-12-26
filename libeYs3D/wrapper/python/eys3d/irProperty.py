"""IR projector control for eYs3D stereo cameras.

Provides control over the infrared projector intensity and extended range mode.
"""
import eys3dPy
from eys3d import logger


class IRProperty:
    """IR projector controller for depth sensing.

    Controls the infrared projector used for structured light depth sensing.
    Supports extended range mode for higher intensity levels.

    Args:
        camera_device: Underlying eys3dPy.CameraDevice instance.

    Example:
        >>> ir = device.get_IRProperty()
        >>> ir.enable_extendIR()  # Enable extended range (0-15)
        >>> ir.set_IR_value(10)   # Set intensity to 10
    """
    def __init__(self, camera_device: eys3dPy.CameraDevice) -> None:
        self.__camera_device = camera_device
        self.__IRProperty: eys3dPy.IRProperty = self.__camera_device.get_IR_property()

    def enable_extendIR(self) -> None:
        """Enable extended IR range mode.

        Extends the IR value range from 0-6 to 0-15.
        """
        self.__IRProperty.enable_extendIR(True)
        self.__camera_device.set_IR_property(self.__IRProperty)
        self.__update_IRProperty()

    def disable_extendIR(self) -> None:
        """Disable extended IR range mode.

        Returns the IR value range to 0-6.
        """
        self.__IRProperty.enable_extendIR(False)
        self.__camera_device.set_IR_property(self.__IRProperty)
        self.__update_IRProperty()

    def is_extendIR_enabled(self) -> bool:
        """Check if extended IR range mode is enabled.

        Returns:
            True if extended range (0-15) is enabled, False for normal (0-6).
        """
        return self.__IRProperty.is_extendIR_enabled()

    def get_IR_value(self) -> int:
        """Get the current IR projector intensity.

        Returns:
            Current IR value (0-6 normal, 0-15 extended).
        """
        return self.__IRProperty.get_IR_value()

    @logger.catch
    def set_IR_value(self, value: int) -> None:
        """Set the IR projector intensity.

        Args:
            value: IR intensity value within valid range.

        Raises:
            ValueError: If value is outside the valid range.
        """
        if not self.get_IR_min() <= value <= self.get_IR_max():
            raise ValueError("Out of range.")
        self.__IRProperty.set_IR_value(value)
        self.__camera_device.set_IR_property(self.__IRProperty)
        self.__update_IRProperty()

    def get_IR_max(self) -> int:
        """Get the maximum IR value.

        Returns:
            Maximum IR value (6 normal, 15 extended).
        """
        return self.__IRProperty.get_IR_max()

    def get_IR_min(self) -> int:
        """Get the minimum IR value.

        Returns:
            Minimum IR value (typically 0).
        """
        return self.__IRProperty.get_IR_min()

    def __update_IRProperty(self) -> None:
        self.__IRProperty = self.__camera_device.get_IR_property()
