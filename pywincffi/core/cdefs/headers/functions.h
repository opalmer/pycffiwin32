//
// NOTE: The tests for this file, tests/test_core/test_cdefs/test_functions.py
//       depend on a function's format to be the following:
//           RETURN_TYPE FunctionName(...
//


// Processes
HANDLE GetCurrentProcess(void);
DWORD GetCurrentProcessId(void);
DWORD GetProcessId(HANDLE);
HANDLE OpenProcess(DWORD, BOOL, DWORD);
BOOL DuplicateHandle(HANDLE, HANDLE, HANDLE, LPHANDLE, DWORD, BOOL, DWORD);

// Pipes
BOOL CreatePipe(PHANDLE, PHANDLE, LPSECURITY_ATTRIBUTES, DWORD);
BOOL SetNamedPipeHandleState(HANDLE, LPDWORD, LPDWORD, LPDWORD);
BOOL GetNamedPipeHandleState(HANDLE, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPTSTR, DWORD);

// IO
BOOL WriteFile(HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED);
BOOL ReadFile(HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED);
BOOL CloseHandle(HANDLE);
