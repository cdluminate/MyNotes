# https://learnxinyminutes.com/docs/cmake/
cmake_minimum_required(VERSION 3.7)
project(learncmake C) # LANG as the second parameter

set(LEARN_CMAKE_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(LEARN_CMAKE_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR})

set(LEARN_CMAKE_VERSION_MAJOR 1)
set(LEARN_CMAKE_VERSION_MINOR 0)
set(LEARN_CMAKE_VERSION_PATCH 0)

# send the configuration to source file
configure_file(
	"${PROJECT_SOURCE_DIR}/learncmakeConfig.h.in"
	"${PROJECT_SOURCE_DIR}/learncmakeConfig.h"
	)

# ~ gcc -I
include_directories(".")

# conditions
set(FLAG ON)
if(FLAG)
	message(STATUS "status")
	#message(WARNING "warning")
	#message(SEND_ERROR "error")
	#message(FATAL_ERROR "fatal")
elseif()
else()
endif()

# for loop
foreach(i a b c)
	message(STATUS ${I})
endforeach(i)

# LOGIC
if(FALSE AND (FALSE OR TRUE))
	message("don't display")
endif()

# compiler condition
if("${CMAKE_C_COMPILER_ID}" STREQUAL "GNU")
	message(STATUS "found GNU compiler, adding specific flags")
	add_definitions( --std=c99 )
endif()

# check OS
if(UNIX)
	message("found UNIX")
endif()
