# Empty3DProject
Simple template for 3D application

# Prerequisites
Build and install prerequisites
https://github.com/spurious/SDL-mirror/tree/release-2.0.8
https://github.com/g-truc/glm
https://github.com/dormon/geGL
https://github.com/dormon/Vars
https://github.com/dormon/BasicCamera
https://github.com/dormon/SDL2CPP
https://github.com/dormon/imguiDormon
https://github.com/dormon/imguiOpenGLDormon
https://github.com/dormon/imguiSDL2Dormon
https://github.com/dormon/imguiSDL2OpenGL
https://github.com/dormon/MealyMachine
https://github.com/dormon/TxtUtils
https://github.com/dormon/ArgumentViewer
https://github.com/dormon/Simple3DApp

# Building Linux
```
$ mkdir build
$ cd build
$ cmake-gui ..
$ # set path to all prerequisites or set CMAKE_INSTALL_PREFIX to directory containing all installed prerequisites
$ make -j4
```
