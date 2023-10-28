#ifndef _PHNT_AMALGAMATE_H
#define _PHNT_AMALGAMATE_H

#ifdef _WINTERNL_
#error Do not mix Winternl.h and phnt.h
#endif // _WINTERNL_
#define _WINTERNL_ // Pretend the header was included

#ifdef _KERNEL_MODE
#define PHNT_DETECTED_MODE PHNT_MODE_KERNEL
#else
#define PHNT_DETECTED_MODE PHNT_MODE_USER
#include <phnt_windows.h>
#endif // _KERNEL_MODE

#ifndef PHNT_MODE
#define PHNT_MODE PHNT_DETECTED_MODE
#endif // PHNT_MODE

#include <phnt.h>

#endif // _PHNT_AMALGAMATE_H
