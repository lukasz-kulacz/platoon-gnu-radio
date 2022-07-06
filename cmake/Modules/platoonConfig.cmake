INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PLATOON platoon)

FIND_PATH(
    PLATOON_INCLUDE_DIRS
    NAMES platoon/api.h
    HINTS $ENV{PLATOON_DIR}/include
        ${PC_PLATOON_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PLATOON_LIBRARIES
    NAMES gnuradio-platoon
    HINTS $ENV{PLATOON_DIR}/lib
        ${PC_PLATOON_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PLATOON DEFAULT_MSG PLATOON_LIBRARIES PLATOON_INCLUDE_DIRS)
MARK_AS_ADVANCED(PLATOON_LIBRARIES PLATOON_INCLUDE_DIRS)

