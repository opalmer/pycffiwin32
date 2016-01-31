"""
Pipe
----

A module for working with pipe objects in Windows.
"""

from collections import namedtuple

from six import integer_types, string_types

from pywincffi.core import dist
from pywincffi.core.checks import Enums, input_check, error_check, NoneType
from pywincffi.exceptions import InputError, WindowsAPIError
from pywincffi.kernel32.handle import INVALID_HANDLE_VALUE

PeekNamedPipeResult = namedtuple(
    "PeekNamedPipeResult",
    ("lpBuffer", "lpBytesRead", "lpTotalBytesAvail",
     "lpBytesLeftThisMessage")
)


def CreatePipe(nSize=0, lpPipeAttributes=None):
    """
    Creates an anonymous pipe and returns the read and write handles.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365152
        https://msdn.microsoft.com/en-us/library/aa379560

    >>> from pywincffi.core import dist
    >>> from pywincffi.kernel32 import CreatePipe
    >>> ffi, library = dist.load()
    >>> lpPipeAttributes = ffi.new(
    ...     "SECURITY_ATTRIBUTES[1]", [{
    ...     "nLength": ffi.sizeof("SECURITY_ATTRIBUTES"),
    ...     "bInheritHandle": True,
    ...     "lpSecurityDescriptor": ffi.NULL
    ...     }]
    ... )
    >>> reader, writer = CreatePipe(lpPipeAttributes=lpPipeAttributes)

    :keyword int nSize:
        The size of the buffer in bytes.  Passing in 0, which is the default
        will cause the system to use the default buffer size.

    :keyword lpPipeAttributes:
        The security attributes to apply to the handle. By default
        ``NULL`` will be passed in meaning then handle we create
        cannot be inherited.  For more detailed information see the links
        below.

    :return:
        Returns a tuple of handles containing the reader and writer
        ends of the pipe that was created.  The user of this function
        is responsible for calling CloseHandle at some point.
    """
    input_check("nSize", nSize, integer_types)
    input_check("lpPipeAttributes", lpPipeAttributes, (NoneType, dict))
    ffi, library = dist.load()

    hReadPipe = ffi.new("PHANDLE")
    hWritePipe = ffi.new("PHANDLE")

    if lpPipeAttributes is None:
        lpPipeAttributes = ffi.NULL

    code = library.CreatePipe(hReadPipe, hWritePipe, lpPipeAttributes, nSize)
    error_check("CreatePipe", code=code, expected=Enums.NON_ZERO)

    return hReadPipe[0], hWritePipe[0]


def SetNamedPipeHandleState(
        hNamedPipe,
        lpMode=None, lpMaxCollectionCount=None, lpCollectDataTimeout=None):
    """
    Sets the read and blocking mode of the specified ``hNamedPipe``.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365787

    :param handle hNamedPipe:
        A handle to the named pipe instance.

    :keyword int lpMode:
        The new pipe mode which is a combination of read mode:

            * ``PIPE_READMODE_BYTE``
            * ``PIPE_READMODE_MESSAGE``

        And a wait-mode flag:

            * ``PIPE_WAIT``
            * ``PIPE_NOWAIT``

    :keyword int lpMaxCollectionCount:
        The maximum number of bytes collected.

    :keyword int lpCollectDataTimeout:
        The maximum time, in milliseconds, that can pass before a
        remote named pipe transfers information
    """
    input_check("hNamedPipe", hNamedPipe, Enums.HANDLE)
    ffi, library = dist.load()

    if lpMode is None:
        lpMode = ffi.NULL
    else:
        input_check("lpMode", lpMode, integer_types)
        lpMode = ffi.new("LPDWORD", lpMode)

    if lpMaxCollectionCount is None:
        lpMaxCollectionCount = ffi.NULL
    else:
        input_check(
            "lpMaxCollectionCount", lpMaxCollectionCount, integer_types)
        lpMaxCollectionCount = ffi.new("LPDWORD", lpMaxCollectionCount)

    if lpCollectDataTimeout is None:
        lpCollectDataTimeout = ffi.NULL
    else:
        input_check(
            "lpCollectDataTimeout", lpCollectDataTimeout, integer_types)
        lpCollectDataTimeout = ffi.new("LPDWORD", lpCollectDataTimeout)

    code = library.SetNamedPipeHandleState(
        hNamedPipe,
        lpMode,
        lpMaxCollectionCount,
        lpCollectDataTimeout
    )
    error_check("SetNamedPipeHandleState", code=code, expected=Enums.NON_ZERO)


def PeekNamedPipe(hNamedPipe, nBufferSize):
    """
    Copies data from a pipe into a buffer without removing it
    from the pipe.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365779

    :param handle hNamedPipe:
        The handele to the pipe object we want to peek into.

    :param int nBufferSize:
        The number of bytes to 'peek' into the pipe.

    :rtype: :class:`PeekNamedPipeResult`
    :return:
        Returns an instance of :class:`PeekNamedPipeResult` which
        contains the buffer read, number of bytes read and the result.
    """
    input_check("hNamedPipe", hNamedPipe, Enums.HANDLE)
    input_check("nBufferSize", nBufferSize, integer_types)
    ffi, library = dist.load()

    # Outputs
    lpBuffer = ffi.new("LPVOID[%d]" % nBufferSize)
    lpBytesRead = ffi.new("LPDWORD")
    lpTotalBytesAvail = ffi.new("LPDWORD")
    lpBytesLeftThisMessage = ffi.new("LPDWORD")

    code = library.PeekNamedPipe(
        hNamedPipe,
        lpBuffer,
        nBufferSize,
        lpBytesRead,
        lpTotalBytesAvail,
        lpBytesLeftThisMessage
    )
    error_check("PeekNamedPipe", code=code, expected=Enums.NON_ZERO)

    return PeekNamedPipeResult(
        lpBuffer=lpBuffer,
        lpBytesRead=lpBytesRead[0],
        lpTotalBytesAvail=lpTotalBytesAvail[0],
        lpBytesLeftThisMessage=lpBytesLeftThisMessage[0]
    )


def GetNamedPipeHandleState(hNamedPipe, is_server_side_pipe=False):
    """
    Retrieves information about named pipe

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365787

    :param handle hNamedPipe:
        The named pipe to return information about.

    :keyword bool is_server_side_pipe:
        If ``hNamedPipe`` is a server side pipe then this keyword
        should be set to True.
    """
    input_check("hNamedPipe", hNamedPipe, Enums.HANDLE)

    ffi, library = dist.load()
    lpMode = ffi.new("LPDWORD")
    lpMaxCollectionCount = ffi.new("LPDWORD")
    lpCollectDataTimeout = ffi.new("LPDWORD")

    if is_server_side_pipe:
        lpCollectDataTimeout = ffi.NULL

    code = library.GetNamedPipeHandleState(
        hNamedPipe, lpMode, lpMaxCollectionCount, lpCollectDataTimeout
    )
    error_check("GetNamedPipeHandleState", code=code, expected=Enums.NON_ZERO)


def CreateNamedPipe(
    lpName, dwOpenMode, dwPipeMode, nMaxInstances, nOutBufferSize,
    nInBufferSize, nDefaultTimeOut=0, lpSecurityAttributes=None
):
    """
    Creates a named pipe object and returns a handle.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365150

    .. warning::

        This function can be called multiple times using the same
        value for ``lpName``.  However, some if the input parameters
        may need to be identical for each call to :func:`CreateNamedPipe`.
        The MSDN documentation above covers this in greater detail.

    :param str lpName:
        The unique name of the named pipe. ``\\.\.pipe\foobar`` for example.

        .. note::

            Be sure you escape your pipe name.  If you want
            ``\\.\pipe\foobar`` as your pipe name, you should provide
            ``\\\\.\\pipe\\foobar``.

    :param int dwOpenMode:
        The mode to open the named pipe in.  See the MSDN documentation
        for possible modes.

    :param int dwPipeMode:
        The mode of the pipe itself ``PIPE_TYPE_BYTE`` or
        ``PIPE_TYPE_MESSAGE`` should be provided here.

    :param int nMaxInstances:
        The maximum number of instances that can be created for this
        pipe.

    :param int nOutBufferSize:
        The reserved size, in bytes, of the output buffer.  See the remarks
        session in MSDN documentation.

    :param int nInBufferSize:
        The reserved size, in bytes, of the input buffer.  See the remarks
        session in MSDN documentation.

    :keyword int nDefaultTimeOut:
        The time-out value, in milliseconds, if :func:`WaitNamedPipe`
        specifies ``NMPWAIT_USE_DEFAULT_WAIT``.  By default we set this to
        ``0`` which will cause the Windows API to use the default value of 50
        milliseconds.

    :keyword LPSECURITY_ATTRIBUTES lpSecurityAttributes:
        A structure used to control access to the named pipe from child
        processes.

    :return:
        Returns the handle to the named pipe object.
    """
    ffi, library = dist.load()

    if lpSecurityAttributes is None:
        lpSecurityAttributes = ffi.NULL

    input_check("lpName", lpName, string_types)
    input_check("dwOpenMode", dwOpenMode, integer_types)
    input_check(
        "dwPipeMode", dwPipeMode, integer_types,
        allowed_values=(library.PIPE_TYPE_BYTE, library.PIPE_TYPE_MESSAGE))
    input_check("nMaxInstances", nMaxInstances, integer_types)
    input_check("nOutBufferSize", nOutBufferSize, integer_types)
    input_check("nInBufferSize", nInBufferSize, integer_types)
    input_check("nDefaultTimeOut", nDefaultTimeOut, integer_types)
    input_check(
        "lpSecurityAttributes", lpSecurityAttributes,
        Enums.SECURITY_ATTRIBUTES
    )

    if not 1 <= nMaxInstances <= library.PIPE_UNLIMITED_INSTANCES:
        raise InputError(
            "nMaxInstances", nMaxInstances, integer_types,
            allowed_values=
            "range 1 to PIPE_UNLIMITED_INSTANCES "
            "(%s)" % library.PIPE_UNLIMITED_INSTANCES)

    handle = library.CreateNamedPipe(
        ffi.cast("LPCTSTR", ffi.new("wchar_t[]", lpName)),
        ffi.cast("DWORD", dwOpenMode),
        ffi.cast("DWORD", dwPipeMode),
        ffi.cast("DWORD", nMaxInstances),
        ffi.cast("DWORD", nOutBufferSize),
        ffi.cast("DWORD", nInBufferSize),
        ffi.cast("DWORD", nDefaultTimeOut),
        lpSecurityAttributes
    )
    if handle == INVALID_HANDLE_VALUE:
        raise WindowsAPIError(
            "CreateNamedPipe", ffi.getwinerror()[-1], INVALID_HANDLE_VALUE,
            "not INVALID_HANDLE_VALUE"
        )

    error_check("CreateNamedPipe")
    return handle
