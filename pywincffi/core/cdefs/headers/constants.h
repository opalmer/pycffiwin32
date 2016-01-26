//
// This file contains constants which can be used either internally or
// by users of pywincffi.
//
// NOTE: The tests for this file, tests/test_core/test_cdefs/test_constants.py
//       depend on a constant's names to follow this format:
//           #define NAME ...
//

// General or system wide constants
#define MAX_PATH ...
#define STD_INPUT_HANDLE ...
#define STD_OUTPUT_HANDLE ...
#define STD_ERROR_HANDLE ...

// Flags for pywincffi.kernel32.process (may be shared with other modules too)
#define PROCESS_CREATE_PROCESS ...
#define PROCESS_CREATE_THREAD ...
#define PROCESS_DUP_HANDLE ...
#define PROCESS_QUERY_INFORMATION ...
#define PROCESS_QUERY_LIMITED_INFORMATION ...
#define PROCESS_SET_INFORMATION ...
#define PROCESS_SET_QUOTA ...
#define PROCESS_SUSPEND_RESUME ...
#define PROCESS_TERMINATE ...
#define PROCESS_VM_OPERATION ...
#define PROCESS_VM_READ ...
#define PROCESS_VM_WRITE ...

// Flags for pywincffi.kernel32.io (may be shared with other modules too)
#define SYNCHRONIZE ...
#define FILE_GENERIC_READ ...
#define FILE_GENERIC_WRITE ...
#define FILE_GENERIC_EXECUTE ...
#define FILE_ADD_FILE ...
#define FILE_ADD_SUBDIRECTORY ...
#define FILE_ALL_ACCESS ...
#define FILE_APPEND_DATA ...
#define FILE_CREATE_PIPE_INSTANCE ...
#define FILE_DELETE_CHILD ...
#define FILE_EXECUTE ...
#define FILE_LIST_DIRECTORY ...
#define FILE_READ_ATTRIBUTES ...
#define FILE_READ_DATA ...
#define FILE_READ_EA ...
#define FILE_TRAVERSE ...
#define FILE_WRITE_ATTRIBUTES ...
#define FILE_WRITE_DATA ...
#define FILE_WRITE_EA ...
#define FILE_SHARE_DELETE ...
#define FILE_SHARE_READ ...
#define FILE_SHARE_WRITE ...
#define FILE_ATTRIBUTE_ARCHIVE ...
#define FILE_ATTRIBUTE_ENCRYPTED ...
#define FILE_ATTRIBUTE_HIDDEN ...
#define FILE_ATTRIBUTE_NORMAL ...
#define FILE_ATTRIBUTE_OFFLINE ...
#define FILE_ATTRIBUTE_READONLY ...
#define FILE_ATTRIBUTE_SYSTEM ...
#define FILE_ATTRIBUTE_TEMPORARY ...
#define FILE_FLAG_BACKUP_SEMANTICS ...
#define FILE_FLAG_DELETE_ON_CLOSE ...
#define FILE_FLAG_NO_BUFFERING ...
#define FILE_FLAG_OPEN_NO_RECALL ...
#define FILE_FLAG_OPEN_REPARSE_POINT ...
#define FILE_FLAG_OVERLAPPED ...
#define FILE_FLAG_POSIX_SEMANTICS ...
#define FILE_FLAG_RANDOM_ACCESS ...
#define FILE_FLAG_SESSION_AWARE ...
#define FILE_FLAG_SEQUENTIAL_SCAN ...
#define FILE_FLAG_WRITE_THROUGH ...
#define CREATE_ALWAYS ...
#define CREATE_NEW ...
#define OPEN_ALWAYS ...
#define OPEN_EXISTING ...
#define TRUNCATE_EXISTING ...

// Flags for pywincffi.kernel32.pipe (may be shared with other modules too)
#define PIPE_TYPE_MESSAGE ...
#define PIPE_READMODE_BYTE ...
#define PIPE_READMODE_MESSAGE ...
#define PIPE_WAIT ...
#define PIPE_NOWAIT ...
#define PIPE_CLIENT_END ...
#define PIPE_SERVER_END ...
#define PIPE_TYPE_BYTE ...
#define PIPE_TYPE_MESSAGE ...

// General security
#define SECURITY_ANONYMOUS ...
#define SECURITY_CONTEXT_TRACKING ...
#define SECURITY_DELEGATION ...
#define SECURITY_EFFECTIVE_ONLY ...
#define SECURITY_IDENTIFICATION ...
#define SECURITY_IMPERSONATION ...
#define STANDARD_RIGHTS_READ ...
#define STANDARD_RIGHTS_WRITE ...
#define GENERIC_ALL ...
#define GENERIC_READ ...
#define GENERIC_WRITE ...

// Errors
#define ERROR_INVALID_PARAMETER ...
#define ERROR_ACCESS_DENIED ...

// For the moment, we can't define this here.  When cffi
// parses the header this returns -1 and cffi seems to
// only handle positive integers right now.
//#define INVALID_HANDLE_VALUE ...
