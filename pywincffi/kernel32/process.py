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

import six

from pywincffi.core.ffi import Library
from pywincffi.core.checks import Enums, input_check, error_check


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
    input_check("dwDesiredAccess", dwDesiredAccess, six.integer_types)
    input_check("bInheritHandle", bInheritHandle, bool)
    input_check("dwProcessId", dwProcessId, six.integer_types)
    ffi, library = Library.load()

    handle_id = library.OpenProcess(
        ffi.cast("DWORD", dwDesiredAccess),
        ffi.cast("BOOL", bInheritHandle),
        ffi.cast("DWORD", dwProcessId)
    )
    error_check("OpenProcess")

    return ffi.new_handle(handle_id)


def GetExitCodeProcess(hProcess):
    """
    Retrieves the termination status of the specified process.

    :param handle hProcess:
        A process handle to return an exit code for.  A result produced by
        :func:`OpenProcess` could be used here for example.

    :returns:
        Returns the exit code for the specified process as an integer.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms683189
    """
    input_check("hProcess", hProcess, Enums.HANDLE)
    ffi, library = Library.load()

    lpExitCode = ffi.new("LPDWORD")
    code = library.GetExitCodeProcess(hProcess, lpExitCode)
    error_check("GetExitCodeProcess", code=code, expected=Enums.NON_ZERO)

    return lpExitCode[0]
