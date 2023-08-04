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
