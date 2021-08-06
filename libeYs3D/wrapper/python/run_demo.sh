VENDOR_SDK_ROOT=../../..
PYTHON_EXECUTE=$(which python3.7)
EYS3D_PYTHON_LIB="$VENDOR_SDK_ROOT/libeYs3D/wrapper/python"
export PYTHONPATH="$PYTHONPATH:$VENDOR_SDK_ROOT/libeYs3D/out:$EYS3D_PYTHON_LIB"

# C++ Engine config path
export EYS3D_HOME="$VENDOR_SDK_ROOT/libeYs3D/out/eYs3D"

# Python Engine config path
export EYS3D_SDK_HOME="$VENDOR_SDK_ROOT/libeYs3D/out/eYs3D"


if [ -z $3 ]
then
	sudo --preserve-env=PYTHONPATH --preserve-env=EYS3D_HOME --preserve-env=EYS3D_SDK_HOME $PYTHON_EXECUTE sample_code/demo.py -m $1 -i $2
else
	sudo --preserve-env=EYS3D_HOME --preserve-env=EYS3D_SDK_HOME --preserve-env=PYTHONPATH  $PYTHON_EXECUTE sample_code/demo.py -m $1 -i $2 --depth-bit $3
fi

