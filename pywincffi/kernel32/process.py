"""
Process
-------

Provides functions, constants and utilities that wrap the Windows
functions associated with process management and interaction.  This
module also provides several constants as well, see Microsoft's
documentation for the constant names and their purpose:

    * **Process Security and Access Rights** -
      https://msdn.microsoft.com/en-us/library/windows/desktop/ms684880

.. note::

    Not all constants may be defined
"""

from six import integer_types

from pywincffi.core.ffi import Library, ffi
from pywincffi.core.checks import Enums, input_check, error_check

kernel32 = Library.load("kernel32")

PROCESS_CREATE_PROCESS = 0x0080
PROCESS_CREATE_THREAD = 0x0002
PROCESS_DUP_HANDLE = 0x0040
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SET_INFORMATION = 0x0200
PROCESS_SET_QUOTA = 0x0100
PROCESS_SUSPEND_RESUME = 0x0800
PROCESS_TERMINATE = 0x0001
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0008
PROCESS_VM_WRITE = 0x0020
SYNCHRONIZE = 0x00100000


def GetCurrentProcess():
    """
    Returns a handle to the current process.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms683179
    """
    return kernel32.GetCurrentProcess()


def GetCurrentProcessId():
    """
    Returns the PID of the current process.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms683180
    """
    return kernel32.GetCurrentProcessId()


def GetProcessId(Process):
    """
    Returns the PID of the current process.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms683215
    """
    input_check("Process", Process, Enums.HANDLE)
    return kernel32.GetProcessId(Process)


def OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId):
    """
    Opens an existing local process object.

    :param int dwDesiredAccess:
        The required access to the process object.

    :param bool bInheritHandle:
        Enables or disable handle inheritance for child processes.

    :param int dwProcessId:
        The id of the local process to be opened.

    :returns:
        Returns a handle to the opened process in the form of
        a void pointer.  This value can be used by other functions
        such as :func:`TerminateProcess`

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms684320
    """
    input_check("dwDesiredAccess", dwDesiredAccess, integer_types)
    input_check("bInheritHandle", bInheritHandle, bool)
    input_check("dwProcessId", dwProcessId, integer_types)

    handle_id = kernel32.OpenProcess(
        ffi.cast("DWORD", dwDesiredAccess),
        ffi.cast("BOOL", bInheritHandle),
        ffi.cast("DWORD", dwProcessId)
    )
    error_check("OpenProcess")

    return ffi.new_handle(handle_id)


# TODO: return value documentation
def DuplicateHandle(
        hSourceProcessHandle, hSourceHandle, hTargetProcessHandle,
        dwDesiredAccess, bInheritHandle, dwOptions=0):
    """
    Duplicates process handles.

    :param handle hSourceProcessHandle:
        A handle to the process owning ``hSourceHandle``.

    :param handle hSourceHandle:
        The handle to be duplicated.

    :param handle hTargetProcessHandle:
        A handle to the process which will receive the
        duplicate ``hSourceHandle``.

    :param int dwDesiredAccess:
        The access rights for the new handle.  This will be ignored
        if ``dwOptions`` specifies ``DUPLICATE_SAME_ACCESS``

    :param bool bInheritHandle:
        True if the handle is inheritable.

    :keyword int dwOptions:
        Optional options which can be zero, the default, or a combination of
        ``DUPLICATE_CLOSE_SOURCE`` or ``DUPLICATE_SAME_ACCESS``

    :return:

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms724251
    """
    input_check("hSourceProcessHandle", hSourceProcessHandle, Enums.HANDLE)
    input_check("hSourceHandle", hSourceHandle, Enums.HANDLE)
    input_check("hTargetProcessHandle", hTargetProcessHandle, Enums.HANDLE)
    input_check("dwDesiredAccess", dwDesiredAccess, integer_types)
    input_check("bInheritHandle", bInheritHandle, bool)
    input_check("dwOptions", dwOptions, integer_types)


