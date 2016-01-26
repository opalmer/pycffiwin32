"""
Pipes
-----

A module containing functions for dealing with pipes.
"""

from collections import namedtuple

from six import integer_types

from pywincffi.core import dist
from pywincffi.core.checks import Enums, input_check, error_check, NoneType

PeekNamedPipeResult = namedtuple(
    "PeekNamedPipeResult",
    ("lpBuffer", "lpBytesRead", "lpTotalBytesAvail", "lpBytesLeftThisMessage")
)
NamedPipeInfo = namedtuple(
    "NamedPipeInfo",
    ("lpFlags", "lpOutBufferSize", "lpInBufferSize", "lpMaxInstances")
)
NamedPipeHandleState = namedtuple(
    "PeekNamedPipeResult",
    ("lpState", "lpCurInstances", "lpMaxCollectionCount",
     "lpCollectDataTimeout", "lpUserName")
)


def CreatePipe(nSize=0, lpPipeAttributes=None):
    """
    Creates an anonymous pipe and returns the read and write handles.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365152
        https://msdn.microsoft.com/en-us/library/aa379560

    >>> from pywincffi.core import dist
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

    # Not covered in tests because
    else:  # pragma: no cover
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


def GetNamedPipeInfo(hNamedPipe):
    """
    Returns information about ``hNamedPipe``

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365445

    :param handle hNamedPipe:
        A handle to the named pipe to return information for.
    """
    input_check("hNamedPipe", hNamedPipe, Enums.HANDLE)

    ffi, library = dist.load()
    lpFlags = ffi.new("LPDWORD")
    lpOutBufferSize = ffi.new("LPDWORD")
    lpInBufferSize = ffi.new("LPDWORD")
    lpMaxInstances = ffi.new("LPDWORD")

    code = library.GetNamedPipeInfo(
        hNamedPipe, lpFlags, lpOutBufferSize, lpInBufferSize, lpMaxInstances)
    error_check("GetNamedPipeInfo", code=code, expected=Enums.NON_ZERO)

    return NamedPipeInfo(
        lpFlags=lpFlags[0],
        lpOutBufferSize=lpOutBufferSize[0],
        lpInBufferSize=lpInBufferSize[0],
        lpMaxInstances=lpMaxInstances[0]
    )


def GetNamedPipeHandleState(hNamedPipe, nMaxUserNameSize=None):
    """
    Retrieves information about the requested ``hNamedPipe`` and
    returns an instance of :class:`NamedPipeHandleState`.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365443

    :param handle hNamedPipe:
        The handle object to return information about.

    :keyword int nMaxUserNameSize:
        Optional size of the buffer to store the user name.
    """
    input_check("hNamedPipe", hNamedPipe, Enums.HANDLE)

    if nMaxUserNameSize is not None:
        input_check("nMaxUserNameSize", nMaxUserNameSize, integer_types)

    ffi, library = dist.load()

    if nMaxUserNameSize is None:
        nMaxUserNameSize = ffi.cast("DWORD", 64)

    # We have to gather some information about the pipe
    # first.  Otherwise we might pass in the wrong values
    # below causing an API failure.


    lpState = ffi.new("LPDWORD")
    lpCurInstances = ffi.new("LPDWORD")
    lpMaxCollectionCount = ffi.new("LPDWORD")
    lpCollectDataTimeout = ffi.new("LPDWORD")
    lpUserName = ffi.new("LPTSTR")

    code = library.GetNamedPipeHandleState(
        hNamedPipe, lpState, lpCurInstances, lpMaxCollectionCount,
        ffi.NULL, ffi.NULL, nMaxUserNameSize
    )
    error_check("GetNamedPipeHandleState", code=code, expected=Enums.NON_ZERO)

    return NamedPipeHandleState(
        lpState=lpState[0],
        lpCurInstances=lpCurInstances[0],
        lpMaxCollectionCount=lpMaxCollectionCount[0]
    )


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
