//
// NOTE: The tests for this file, tests/test_core/test_cdefs/test_functions.py
//       depend on a function's format to be the following:
//           RETURN_TYPE FunctionName(...
//

// Custom functions
VOID SetLastError(DWORD);

// Processes
HANDLE OpenProcess(DWORD, BOOL, DWORD);
HANDLE GetCurrentProcess();
DWORD GetProcessId(HANDLE);

// Pipes
BOOL CreatePipe(PHANDLE, PHANDLE, LPSECURITY_ATTRIBUTES, DWORD);
BOOL PeekNamedPipe(HANDLE, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD);
BOOL GetNamedPipeInfo(HANDLE, LPDWORD, LPDWORD, LPDWORD, LPDWORD);
BOOL SetNamedPipeHandleState(HANDLE, LPDWORD, LPDWORD, LPDWORD);
BOOL GetNamedPipeHandleState(
    HANDLE, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPTSTR, DWORD);

// Files
BOOL WriteFile(HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED);
BOOL ReadFile(HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED);

// Handles
HANDLE handle_from_fd(int);
BOOL CloseHandle(HANDLE);
HANDLE GetStdHandle(DWORD);
