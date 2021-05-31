import os


def get_EYS3D_HOME():
    """Return EYS3D_HOME path.

    If user do not specify path, default path of EYS3D_HOME is at `~/.eYs3D`.

    Returns:
        str: The path of EYS3D_HOME.
    """
    try:
        EYS3D_HOME = os.environ['EYS3D_HOME']
    except KeyError:
        EYS3D_HOME = os.path.join(os.path.expanduser("~"), ".eYs3D")
    return EYS3D_HOME


def get_EYS3D_SDK_HOME():
    """Return EYS3D_SDK_HOME path.

    This environment variable would set when eys3d system created.

    Returns:
        str: The path of EYS3D_SDK_HOME.
    """
    EYS3D_SDK_HOME = os.environ['EYS3D_SDK_HOME']
    return EYS3D_SDK_HOME
