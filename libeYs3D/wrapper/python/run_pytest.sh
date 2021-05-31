#!/bin/sh

VENDOR_SDK_ROOT=../../..
PYTHON_EXECUTE=$(which python3.7)
export PYTHONPATH=$VENDOR_SDK_ROOT/libeYs3D/out:$PYTHONPATH

if [ $1 = 8062 ] 
then
	TEST_FILE="test/test_eYs3DLib_8062.py"
elif [ $1 = 8053 ]
then
	TEST_FILE="test/test_eYs3DLib_8053.py"
else
	echo "Please input module (8053/8062) "
	exit
fi

sudo --preserve-env=PYTHONPATH $PYTHON_EXECUTE -m pytest $TEST_FILE
