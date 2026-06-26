"""Camera property control for eYs3D stereo cameras.

Provides access to camera exposure, white balance, and light source controls.
"""
from typing import Dict
import eys3dPy


class CameraProperty:
    """Camera property controller for exposure, white balance, and light settings.

    Provides control over UVC camera properties including auto/manual exposure,
    auto/manual white balance, low light compensation, and light source frequency.

    Args:
        camera_device: Underlying eys3dPy.CameraDevice instance.

    Example:
        >>> prop = device.get_cameraProperty()
        >>> prop.enable_AE()  # Enable auto exposure
        >>> temp = prop.get_white_balance_temperature()  # 2800-6500K
    """
    def __init__(self, camera_device: eys3dPy.CameraDevice) -> None:
        self.__camera_device = camera_device

    def enable_AE(self) -> None:
        """Enable auto exposure mode."""
        self.__camera_device.enable_AE()

    def disable_AE(self) -> None:
        """Disable auto exposure mode."""
        self.__camera_device.disable_AE()

    def get_AE_status(self) -> bool:
        """Get the status of auto exposure.

        Returns:
            True if auto exposure is enabled, False otherwise.
        """
        return self.__camera_device.get_AE_status()

    def get_exposure_value(self) -> int:
        """Get the exposure value (log2 scale).

        Returns:
            Exposure value in range -13 to 3.
        """
        return self.__camera_device.get_exposure_value()

    def set_exposure_value(self, value: int) -> None:
        """Set the exposure value.

        Values outside the valid range are clamped to min/max.

        Args:
            value: Exposure value in range -13 to 3.
        """
        val_range = self.get_exposure_range()
        if value >= val_range['Max']:
            value = val_range['Max']
        elif value <= val_range['Min']:
            value = val_range['Min']
        self.__camera_device.set_exposure_value(value)

    def get_manual_exposure_time(self) -> float:
        """Get the manual exposure time.

        Returns:
            Exposure time in device-specific units.
        """
        return self.__camera_device.get_manual_exposure_time()

    def set_manual_exposure_time(self, value: float) -> None:
        """Set the manual exposure time.

        Args:
            value: Exposure time in device-specific units.
        """
        self.__camera_device.set_manual_exposure_time(value)

    def get_manual_global_gain(self) -> float:
        """Get the manual global gain.

        Returns:
            Global gain value in device-specific units.
        """
        return self.__camera_device.get_manual_global_gain()

    def set_manual_global_gain(self, value: float) -> None:
        """Set the manual global gain.

        Args:
            value: Global gain value in device-specific units.
        """
        self.__camera_device.set_manual_global_gain(value)

    def get_exposure_range(self) -> Dict[str, int]:
        """Get the exposure value range.

        Returns:
            Dictionary with keys: 'Max', 'Min', 'Step', 'Default'.
        """
        return self.__camera_device.get_exposure_range()

    def enable_AWB(self) -> None:
        """Enable auto white balance mode."""
        self.__camera_device.enable_AWB()

    def disable_AWB(self) -> None:
        """Disable auto white balance mode."""
        self.__camera_device.disable_AWB()

    def get_AWB_status(self) -> bool:
        """Get the status of auto white balance.

        Returns:
            True if auto white balance is enabled, False otherwise.
        """
        return self.__camera_device.get_AWB_status()

    def get_white_balance_temperature(self) -> int:
        """Get the white balance temperature.

        Returns:
            White balance temperature in Kelvin (2800-6500K).
        """
        return self.__camera_device.get_white_balance_temperature()

    def set_white_balance_temperature(self, value: int) -> None:
        """Set the white balance temperature.

        Args:
            value: Temperature in Kelvin (2800-6500K).

        Raises:
            ValueError: If value is outside the valid range.
        """
        range_temperature = self.__camera_device.get_white_balance_temperature_range()
        if value not in range(range_temperature['Min'],
                              range_temperature['Max'] + 1):
            raise ValueError("Out of range.")
        self.__camera_device.set_white_balance_temperature(value)

    def get_white_balance_temperature_range(self) -> Dict[str, int]:
        """Get the white balance temperature range.

        Returns:
            Dictionary with keys: 'Max', 'Min', 'Step', 'Default'.
        """
        return self.__camera_device.get_white_balance_temperature_range()

    def get_low_light_compensation_status(self) -> bool:
        """Get the status of low light compensation.

        Returns:
            True if low light compensation is enabled, False otherwise.
        """
        return self.__camera_device.get_low_light_compensation_status()

    def enable_low_light_compensation(self) -> None:
        """Enable low light compensation mode."""
        self.__camera_device.set_low_light_compensation(1)

    def disable_low_light_compensation(self) -> None:
        """Disable low light compensation mode."""
        self.__camera_device.set_low_light_compensation(0)

    def get_light_source_status(self) -> eys3dPy.LIGHT_SOURCE_VALUE:
        """Get the light source frequency setting.

        Returns:
            LIGHT_SOURCE_VALUE.VALUE_50HZ or LIGHT_SOURCE_VALUE.VALUE_60HZ.
        """
        return eys3dPy.LIGHT_SOURCE_VALUE(
            self.__camera_device.get_light_source_status())

    def set_light_source(self, value: eys3dPy.LIGHT_SOURCE_VALUE) -> None:
        """Set the light source frequency.

        Args:
            value: LIGHT_SOURCE_VALUE.VALUE_50HZ or LIGHT_SOURCE_VALUE.VALUE_60HZ.
        """
        self.__camera_device.set_light_source(value)
