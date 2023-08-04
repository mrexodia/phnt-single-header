#ifndef _PHNT_AMALGAMATE_H
#define _PHNT_AMALGAMATE_H

#ifdef _WINTERNL_
#error Do not mix Winternl.h and phnt.h
#endif // _WINTERNL_
#define _WINTERNL_ // Pretend the header was included

#include <phnt_windows.h>
#include <phnt.h>

#endif // _PHNT_AMALGAMATE_H
