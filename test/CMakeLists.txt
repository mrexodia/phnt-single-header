cmake_minimum_required(VERSION 3.15)

set(phnt_HEADER "${CMAKE_SOURCE_DIR}/../out/phnt.h")
if(NOT EXISTS "${phnt_HEADER}")
    message(FATAL_ERROR "Could not find ../out/phnt.h, to generate: python amalgamate.py")
endif()

file(COPY "${phnt_HEADER}" DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}")

project(phnt-test)

function(phnt_test target)
    add_executable(${target} ${ARGN})
    target_link_options(${target} PRIVATE "/NODEFAULTLIB")
    target_link_options(${target} PRIVATE "/ENTRY:EntryPoint")
    target_link_libraries(${target} PRIVATE ntdll.lib)
endfunction()

phnt_test(test-c test.c)
phnt_test(test-cpp test.cpp)
