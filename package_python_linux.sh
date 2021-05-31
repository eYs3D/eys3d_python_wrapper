ROOT=$(pwd)
FOLDER="$ROOT"/release
mkdir -p "$FOLDER"

VERSION_TXT="$FOLDER"/version.txt
touch "$VERSION_TXT"
echo "$(git log -n1 --pretty=format:"%h")" >> "$VERSION_TXT"

echo $ROOT
echo $FOLDER

cp -r "$ROOT"/libeYs3D/wrapper "$FOLDER"
cp -r "$ROOT"/libeYs3D/out "$FOLDER"
cp -r "$ROOT"/libeYs3D/src "$FOLDER"
sudo rm -rf "$ROOT"/libeYs3D/*
find . -name "*.cpp" -type f -delete
find . -name "*.c" -type f -delete
cp -r $FOLDER/* "$ROOT"/libeYs3D/

rm -rf "$FOLDER"/venv
rm -rf "$FOLDER"/pybind11
rm -rf "$FOLDER"/cmake*
rm "$FOLDER"/README.cgroup
rm "$FOLDER"/README.engine_tick_trace
rm "$FOLDER"/run_callback.bat
rm "$FOLDER"/run_callback.sh
rm "$FOLDER"/run_frameset_pipeline.bat
rm "$FOLDER"/run_frameset_pipeline.sh
rm "$FOLDER"/run_pipeline.bat
rm "$FOLDER"/run_pipeline.sh
rm "$FOLDER"/run_test.bat
rm "$FOLDER"/run_test.sh

sudo rm -rf lib
sudo rm -rf include
sudo rm -rf eSPDI_win64
sudo rm -rf eSPDI
sudo rm -rf dirent
sudo rm -rf .gitignore
sudo rm -rf .gitmodules
sudo rm -rf cmake-build-release
sudo rm -rf cmake-build-debug
sudo rm -rf CMakeLists.txt
sudo rm -rf cfg
sudo rm -rf build_python.sh
sudo rm -rf build_python
sudo rm -rf build_unity.bat
sudo rm -rf build.sh
sudo rm -rf build.bat
sudo rm -rf bin
sudo rm -rf log4cplus

rm -rf "$FOLDER"
