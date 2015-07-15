typedef struct _SECURITY_ATTRIBUTES {
    DWORD  nLength;
    LPVOID lpSecurityDescriptor;
    BOOL   bInheritHandle;
} SECURITY_ATTRIBUTES, *PSECURITY_ATTRIBUTES, *LPSECURITY_ATTRIBUTES;

typedef struct _OVERLAPPED {
    ULONG_PTR Internal;
    ULONG_PTR InternalHigh;
    union {
        struct {
            DWORD Offset;
            DWORD OffsetHigh;
        };
        PVOID    Pointer;
    };
    HANDLE        hEvent;
} OVERLAPPED, *LPOVERLAPPED;

// Processes
HANDLE GetCurrentProcess(void);
DWORD GetCurrentProcessId(void);
DWORD GetProcessId(HANDLE);
BOOL OpenProcess(DWORD, BOOL, DWORD);

// IO
BOOL CreatePipe(PHANDLE, PHANDLE, LPSECURITY_ATTRIBUTES, DWORD);
BOOL CloseHandle(HANDLE);
BOOL WriteFile(HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED);
BOOL ReadFile(HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED);
