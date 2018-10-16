# Empty3DProject
Simple template for 3D application

# Prerequisites
Build and install prerequisites
https://github.com/spurious/SDL-mirror/tree/release-2.0.8 <br>
https://github.com/g-truc/glm <br>
https://github.com/dormon/geGL <br>
https://github.com/dormon/Vars <br>
https://github.com/dormon/BasicCamera <br>
https://github.com/dormon/SDL2CPP <br>
https://github.com/dormon/imguiDormon <br>
https://github.com/dormon/imguiOpenGLDormon <br>
https://github.com/dormon/imguiSDL2Dormon <br>
https://github.com/dormon/imguiSDL2OpenGL <br>
https://github.com/dormon/MealyMachine <br>
https://github.com/dormon/TxtUtils <br>
https://github.com/dormon/ArgumentViewer <br>
https://github.com/dormon/Simple3DApp <br>
http://freeimage.sourceforge.net/ <br>

You can build most of the prerequisites using python script
```
./downloadAndInstallPrerequisites.py
```
The script will download repositories into externRepositories directory and
will install all github repositories into install directory

# Building Linux
```
$ mkdir build
$ cd build
$ cmake-gui ..
$ # set path to all prerequisites (*_DIR) or set CMAKE_INSTALL_PREFIX to directory containing all installed prerequisites
$ # choose DEBUG or RELEASE CMAKE_BUILD_TYPE
$ make -j4
```
