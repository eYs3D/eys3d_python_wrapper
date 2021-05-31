class RemoveCurve:
    """Perform curve removal function.

    [TODO][EYS3D][DOC] Description in detail. 
    
    Args:
       camera_device (obj): CameraDevice.
       depthFilterOptions (obj): DepthFilterOptions.

    """
    def __init__(self, camera_device, depthFilterOptions):
        self.__camera_device = camera_device
        self.__depthFilterOptions = depthFilterOptions

    def enable(self, ):
        """Enable remove curve.

        To enable remove curve.
        """
        self.__depthFilterOptions.enable_flyingDepthCancellation(True)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def disable(self, ):
        """Disable remove curve.

        To disable remove curve.
        """
        self.__depthFilterOptions.enable_flyingDepthCancellation(False)
        self.__camera_device.set_depthFilterOptions(self.__depthFilterOptions)

    def is_enabled(self):
        """Check the status.

        To check the status of remove curve function.

        Returns:
            bool: True for enable. False otherwise.
        """
        return self.__depthFilterOptions.is_flyingDepthCancellation_enabled()
