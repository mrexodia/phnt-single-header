cmake_minimum_required(VERSION 3.15)

set(phnt_DIR "${CMAKE_SOURCE_DIR}/../out")
if(NOT EXISTS "${phnt_DIR}/phnt.h")
    message(FATAL_ERROR "Could not find ../out/phnt.h, to generate: python amalgamate.py")
endif()

#file(COPY "${phnt_HEADER}" DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}")

# Default to a Release build
if(GENERATOR_IS_MULTI_CONFIG)
    set(CMAKE_CONFIGURATION_TYPES "Release" CACHE STRING "")
elseif(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

project(phnt-test)

function(phnt_test target)
    add_executable(${target} ${ARGN})
    target_link_libraries(${target} PRIVATE ntdll.lib)
    target_include_directories(${target} PRIVATE "${phnt_DIR}")
    target_link_options(${target} PRIVATE "/NODEFAULTLIB")
    target_link_options(${target} PRIVATE "/ENTRY:EntryPoint")
endfunction()

phnt_test(test-c test.c)
phnt_test(test-cpp test.cpp)
