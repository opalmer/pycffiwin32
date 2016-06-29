#include <io.h>
#include <winsock2.h>
#include <winerror.h>
#include <windows.h>
#include <TlHelp32.h>
#include <Python.h>

// Copied from Python's socket module.  These are used to determine
// how PyLong_FromSocket_t should be defined.
#ifdef MS_WIN64
#define SIZEOF_SOCKET_T 8
#else
#define SIZEOF_SOCKET_T 4
#endif

// Copied from Python's socket module.  These are considered private so we
// wouldn't have been able to used them directly.  The resulting function,
// PyLong_FromSocket_t, is used in socket_from_fd below.
#if SIZEOF_SOCKET_T <= SIZEOF_LONG
#define PyLong_FromSocket_t(fd) PyLong_FromLong((SOCKET)(fd))
#else
#define PyLong_FromSocket_t(fd) PyLong_FromLongLong((SOCKET)(fd))
#endif


// Extra constants which are not defined in all versions of the Windows
// SDK.  If cffi fails to find the value, it ends up being picked up from
// here.
#if !defined(FILE_FLAG_SESSION_AWARE)
    static const int FILE_FLAG_SESSION_AWARE = 0x00800000;
#endif

#if !defined(STARTF_UNTRUSTEDSOURCE)
    static const int STARTF_UNTRUSTEDSOURCE = 0x00008000;
#endif

#if !defined(STARTF_PREVENTPINNING)
    static const int STARTF_PREVENTPINNING = 0x00002000;
#endif

#if !defined(STARTF_TITLEISAPPID)
    static const int STARTF_TITLEISAPPID = 0x00001000;
#endif

#if !defined(STARTF_TITLEISLINKNAME)
    static const int STARTF_TITLEISLINKNAME = 0x00000800;
#endif

HANDLE handle_from_fd(int fd) {
    return (HANDLE)_get_osfhandle(fd);
}


// Takes a file descriptor from a Python socket and converts
// it to a Windows SOCKET object.
HANDLE socket_from_fd(int fd) {
    int value = (int)PyLong_FromSocket_t(fd);
    return handle_from_fd(value);
}
