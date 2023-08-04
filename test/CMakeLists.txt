# NOTE: This code is hacky because it's used for tests.
# If you are looking for an example, check the README.

cmake_minimum_required(VERSION 3.15)

# Check that amalgamate.py was run
set(phnt_DIR "${CMAKE_SOURCE_DIR}/../out")
if(NOT EXISTS "${phnt_DIR}/phnt.h")
    message(FATAL_ERROR "Could not find ../out/phnt.h, to generate: python amalgamate.py")
endif()

# Default to a Release build
if(GENERATOR_IS_MULTI_CONFIG)
    set(CMAKE_CONFIGURATION_TYPES "Release" CACHE STRING "")
elseif(NOT DEFINED CACHE{CMAKE_BUILD_TYPE})
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "")
endif()

option(PHNT_TEST_PACKAGE "Test package mode" OFF)

project(phnt-test)

if(PHNT_TEST_PACKAGE)
    set(PACKAGE_DIR "${PROJECT_BINARY_DIR}/phnt")
    file(REMOVE_RECURSE "${PACKAGE_DIR}")
    message(STATUS "Configuring phnt package...")
    execute_process(
        COMMAND "${CMAKE_COMMAND}" -B "${PACKAGE_DIR}/build" -S "${phnt_DIR}" -G Ninja "-DCMAKE_BUILD_TYPE=Release"
        RESULT_VARIABLE PACKAGE_STATUS
    )
    if(NOT PACKAGE_STATUS EQUAL 0)
        message(FATAL_ERROR "Failed to configure phnt package!")
    endif()
    message(STATUS "Installing phnt package...")
    execute_process(
        COMMAND "${CMAKE_COMMAND}" --install "${PACKAGE_DIR}/build" --prefix "${PACKAGE_DIR}/install"
        RESULT_VARIABLE PACKAGE_STATUS
    )
    if(NOT PACKAGE_STATUS EQUAL 0)
        message(FATAL_ERROR "Failed to install phnt package!")
    endif()
    set(CMAKE_PREFIX_PATH "${PACKAGE_DIR}/install")
    find_package(phnt REQUIRED)
else()
    add_subdirectory("${phnt_DIR}" "${PROJECT_BINARY_DIR}/phnt")
endif()

function(phnt_test target)
    add_executable(${target} ${ARGN})
    target_link_libraries(${target} PRIVATE phnt::phnt)
    target_link_options(${target} PRIVATE "/NODEFAULTLIB")
    target_link_options(${target} PRIVATE "/ENTRY:EntryPoint")
endfunction()

phnt_test(test-c test.c)
phnt_test(test-cpp test.cpp)
