VENDOR_SDK_ROOT=../../..
PYTHON_EXECUTE=$(which python3.7)
EYS3D_PYTHON_LIB="$VENDOR_SDK_ROOT/libeYs3D/wrapper/python"
export PYTHONPATH="$PYTHONPATH:$VENDOR_SDK_ROOT/libeYs3D/out:"

if [ -z $3 ]
then
	sudo --preserve-env=PYTHONPATH $PYTHON_EXECUTE sample_code/demo.py -m $1 -i $2  
else
	sudo --preserve-env=PYTHONPATH $PYTHON_EXECUTE sample_code/demo.py -m $1 -i $2 --depth-bit $3 
fi

