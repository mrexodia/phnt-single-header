# phnt-single-header

This repository automatically generates a single-header version of [System Informer](https://github.com/winsiderss/systeminformer)'s [phnt](https://github.com/winsiderss/systeminformer/tree/master/phnt) library. This repository was created because the original library is separated in many headers and can be annoying to integrate into your project.

## Usage

This is a simple example of using phnt

```c
#define PHNT_VERSION PHNT_WIN11
#include "phnt.h" // Instead of Windows.h

// Imports for ntdll.dll
#pragma comment(lib, "ntdll.lib")

static char message[] = "Hello, phnt!\r\n";

int main()
{
    IO_STATUS_BLOCK IoStatusBlock = { 0, 0 };
    NtWriteFile(
        NtCurrentPeb()->ProcessParameters->StandardOutput,
        NULL,
        NULL,
        NULL,
        &IoStatusBlock,
        message,
        strlen(message) - 1,
        NULL,
        NULL
    );
    return 0;
}
```

## Download

[`phnt.h`](https://github.com/mrexodia/phnt-single-header/releases/latest/download/phnt.h) (direct link to the [latest release](https://github.com/mrexodia/phnt-single-header/releases/latest)).

## CMake

To quickly use this library from CMake, use [FetchContent](https://cmake.org/cmake/help/latest/module/FetchContent.html):

```cmake
cmake_minimum_required(VERSION 3.24)
cmake_policy(SET CMP0135 NEW)
project(phnt-example)

include(FetchContent)
set(phnt_TAG "v1.2-4d1b102f")
message(STATUS "Fetching phnt (${phnt_TAG})...")
FetchContent_Declare(phnt
    URL "https://github.com/mrexodia/phnt-single-header/releases/download/${phnt_TAG}/phnt.zip"
    URL_HASH "SHA256=ccd3cbc27c83b2870f6c8d2b72d47cc75a38fc7bb57b11fc9677a9ec46710e10"
)
FetchContent_MakeAvailable(phnt)

add_executable(example main.cpp)
target_link_libraries(example PRIVATE phnt::phnt)
```

Instead of `FetchContent` you can also extract [`phnt.zip`](https://github.com/mrexodia/phnt-single-header/releases/latest/download/phnt.zip) to `third_party/phnt` in your project and do:

```cmake
add_subdirectory(third_party/phnt)
```

The target `phnt::phnt` also links to `ntdll.lib`. If you want to avoid this you can link to `phnt::headers` instead.

<sub>_Note_: The CMake project in `phnt.zip` also works as a CMake package. After configuring and installing it, you can do `find_package(phnt REQUIRED)` and everything should work out of the box.</sub>

## Older SDKs

To use phnt with older SDK versions, change the `PHNT_VERSION` to one of the following:

```
#define PHNT_VERSION PHNT_WIN2K
#define PHNT_VERSION PHNT_WINXP
#define PHNT_VERSION PHNT_WS03
#define PHNT_VERSION PHNT_VISTA
#define PHNT_VERSION PHNT_WIN7
#define PHNT_VERSION PHNT_WIN8
#define PHNT_VERSION PHNT_WINBLUE
#define PHNT_VERSION PHNT_THRESHOLD
#define PHNT_VERSION PHNT_THRESHOLD2
#define PHNT_VERSION PHNT_REDSTONE
#define PHNT_VERSION PHNT_REDSTONE2
#define PHNT_VERSION PHNT_REDSTONE3
#define PHNT_VERSION PHNT_REDSTONE4
#define PHNT_VERSION PHNT_REDSTONE5
#define PHNT_VERSION PHNT_19H1
#define PHNT_VERSION PHNT_19H2
#define PHNT_VERSION PHNT_20H1
#define PHNT_VERSION PHNT_20H2
#define PHNT_VERSION PHNT_21H1
#define PHNT_VERSION PHNT_WIN10_21H2
#define PHNT_VERSION PHNT_WIN10_22H2
#define PHNT_VERSION PHNT_WIN11
#define PHNT_VERSION PHNT_WIN11_22H2
```
