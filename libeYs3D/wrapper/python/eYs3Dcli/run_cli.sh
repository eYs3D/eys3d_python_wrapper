PYTHON_EXECUTE=$(which python3.7)
VENDOR_SDK_ROOT=../../../..
EYS3D_PYTHON_LIB="$VENDOR_SDK_ROOT/libeYs3D/wrapper/python"
export PYTHONPATH="$PYTHONPATH:$VENDOR_SDK_ROOT/libeYs3D/out:$EYS3D_PYTHON_LIB:."

# C++ Engine config path
export EYS3D_HOME="$VENDOR_SDK_ROOT/libeYs3D/out/eYs3D"

# Python Engine config path
export EYS3D_SDK_HOME="$VENDOR_SDK_ROOT/libeYs3D/out/eYs3D"

sudo --preserve-env=EYS3D_HOME --preserve-env=EYS3D_SDK_HOME --preserve-env=PYTHONPATH $PYTHON_EXECUTE scripts/eYs3Dcli --version

