//
// NOTE: The tests for this file, tests/test_core/test_cdefs/test_functions.py
//       depend on a function's format to be the following:
//           RETURN_TYPE FunctionName(...
//


// Processes
HANDLE OpenProcess(DWORD, BOOL, DWORD);
BOOL GetExitCodeProcess(HANDLE, LPDWORD);

// Pipes
BOOL CreatePipe(PHANDLE, PHANDLE, LPSECURITY_ATTRIBUTES, DWORD);
BOOL PeekNamedPipe(HANDLE, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD);
BOOL SetNamedPipeHandleState(HANDLE, LPDWORD, LPDWORD, LPDWORD);

// Files
BOOL WriteFile(HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED);
BOOL ReadFile(HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED);
BOOL LockFileEx(HANDLE, DWORD, DWORD, DWORD, DWORD, LPOVERLAPPED);

// Misc IO
BOOL CloseHandle(HANDLE);
HANDLE GetStdHandle(DWORD);

// Custom functions
HANDLE handle_from_fd(int);
