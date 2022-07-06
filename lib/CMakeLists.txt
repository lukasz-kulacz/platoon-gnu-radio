# Copyright 2011,2012,2016 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})

list(APPEND platoon_sources
)

set(platoon_sources "${platoon_sources}" PARENT_SCOPE)
if(NOT platoon_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT platoon_sources)

add_library(gnuradio-platoon SHARED ${platoon_sources})
target_link_libraries(gnuradio-platoon ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-platoon PROPERTIES DEFINE_SYMBOL "gnuradio_platoon_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-platoon PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-platoon RUNTIME_COMPONENT "platoon_runtime" DEVEL_COMPONENT "platoon_devel")

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_platoon_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_platoon.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_platoon.cc
)

add_executable(test-platoon ${test_platoon_sources})

target_link_libraries(
  test-platoon
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  gnuradio-platoon
)

GR_ADD_TEST(test_platoon test-platoon)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")

