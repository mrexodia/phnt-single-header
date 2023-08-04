#define PHNT_VERSION PHNT_WIN11
#include "phnt.h"

#ifdef __cplusplus
static char message[] = "Hello from phnt in C++\r\n";
#else
static char message[] = "Hello from phnt in C\r\n";
#endif // __cplusplus

extern int EntryPoint(PPEB peb)
{
    IO_STATUS_BLOCK IoStatusBlock = { 0, 0 };
    NtWriteFile(
        peb->ProcessParameters->StandardOutput,
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
