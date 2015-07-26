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

from pywincffi.core.ffi import Library
from pywincffi.core.checks import Enums, input_check, error_check


def GetCurrentProcess():
    """
    Returns a handle to the current process.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms683179
    """
    _, library = Library.load()
    return library.GetCurrentProcess()


def GetCurrentProcessId():
    """
    Returns the PID of the current process.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms683180
    """
    _, library = Library.load()
    return library.GetCurrentProcessId()


def GetProcessId(Process):
    """
    Returns the PID of the current process.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms683215
    """
    input_check("Process", Process, Enums.HANDLE)
    _, library = Library.load()

    return library.GetProcessId(Process)


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
    ffi, library = Library.load()

    handle_id = library.OpenProcess(
        ffi.cast("DWORD", dwDesiredAccess),
        ffi.cast("BOOL", bInheritHandle),
        ffi.cast("DWORD", dwProcessId)
    )
    error_check("OpenProcess")

    return ffi.new_handle(handle_id)


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
        Optional values which can be zero, the default, or a combination of
        ``DUPLICATE_CLOSE_SOURCE`` and/or ``DUPLICATE_SAME_ACCESS``

    :return:
        Returns a ``LPHANDLE`` object which contains the duplicate handle

    .. seealso::

        https://msdn.microsoft.com/en-us/library/windows/desktop/ms724251
    """
    input_check("hSourceProcessHandle", hSourceProcessHandle, Enums.HANDLE)
    input_check("hSourceHandle", hSourceHandle, Enums.HANDLE)
    input_check("hTargetProcessHandle", hTargetProcessHandle, Enums.HANDLE)
    input_check("dwDesiredAccess", dwDesiredAccess, integer_types)
    input_check("bInheritHandle", bInheritHandle, bool)
    input_check("dwOptions", dwOptions, integer_types)
    ffi, library = Library.load()

    lpTargetHandle = ffi.new("LPHANDLE")
    code = library.DuplicateHandle(
        hSourceProcessHandle, hSourceHandle, hTargetProcessHandle,
        lpTargetHandle, dwDesiredAccess, bInheritHandle, dwOptions
    )
    error_check("DuplicateHandle", code=code, expected=Enums.NON_ZERO)
    return lpTargetHandle


