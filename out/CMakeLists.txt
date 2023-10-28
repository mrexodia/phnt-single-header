cmake_minimum_required(VERSION 3.5)

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
	message(FATAL_ERROR "In-tree builds are not supported. Run CMake from a separate directory: cmake -B build")
endif()

set(PROJECT_IS_TOP_LEVEL OFF)
if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
	set(PROJECT_IS_TOP_LEVEL ON)
endif()

project(phnt VERSION 3.0)

if(PROJECT_IS_TOP_LEVEL)
    set(tgt_headers headers)
else()
    set(tgt_headers phnt_headers)
endif()

add_library(${tgt_headers} INTERFACE)
add_library(${PROJECT_NAME}::headers ALIAS ${tgt_headers})
target_include_directories(${tgt_headers} SYSTEM INTERFACE
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}>
)
target_include_directories(${tgt_headers} INTERFACE
    $<INSTALL_INTERFACE:$<INSTALL_PREFIX>/include>
)

add_library(phnt INTERFACE)
add_library(${PROJECT_NAME}::phnt ALIAS phnt)
target_link_libraries(phnt INTERFACE phnt::headers)

if(MSVC)
    target_link_libraries(phnt INTERFACE "ntdll.lib")
endif()

# References:
# - https://dominikberner.ch/cmake-interface-lib/
# - https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html
if(PROJECT_IS_TOP_LEVEL)
    include(GNUInstallDirs)
    install(
        TARGETS
            phnt
            ${tgt_headers}
        EXPORT
            ${PROJECT_NAME}_Targets
        ARCHIVE
            DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY
            DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME
            DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
    include(CMakePackageConfigHelpers)
    write_basic_package_version_file(
        "${PROJECT_NAME}ConfigVersion.cmake"
        VERSION
            ${PROJECT_VERSION}
        COMPATIBILITY
            SameMajorVersion
    )
    set(CONFIG_IN_CONTENTS "@PACKAGE_INIT@\n\ninclude(\"\$\{CMAKE_CURRENT_LIST_DIR\}/@PROJECT_NAME@Targets.cmake\")\n\ncheck_required_components(\"@PROJECT_NAME@\")")
    set(CONFIG_IN_PATH "${PROJECT_BINARY_DIR}/${PROJECT_NAME}Config.cmake.in")
    file(WRITE "${CONFIG_IN_PATH}" "${CONFIG_IN_CONTENTS}")
    configure_package_config_file(
        "${CONFIG_IN_PATH}" "${PROJECT_NAME}Config.cmake"
        INSTALL_DESTINATION
            "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}"
    )
    install(
        EXPORT
            ${PROJECT_NAME}_Targets
        FILE
            "${PROJECT_NAME}Targets.cmake"
        NAMESPACE
            ${PROJECT_NAME}::
        DESTINATION
            "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}"
    )
    install(
        FILES
            "${PROJECT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
            "${PROJECT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
        DESTINATION
            "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}"
    )
    install(
        FILES
            "${PROJECT_SOURCE_DIR}/phnt.h"
        DESTINATION
            "${CMAKE_INSTALL_INCLUDEDIR}"
    )
endif()
