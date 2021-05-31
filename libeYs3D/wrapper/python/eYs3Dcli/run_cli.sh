PYTHON_EXECUTE=$(which python3.7)
VENDOR_SDK_ROOT=../../../..
export PYTHONPATH=$VENDOR_SDK_ROOT/libeYs3D/wrapper/python:$VENDOR_SDK_ROOT/libeYs3D/out:$PYTHONPATH

sudo --preserve-env=PYTHONPATH $PYTHON_EXECUTE scripts/eYs3Dcli --version

