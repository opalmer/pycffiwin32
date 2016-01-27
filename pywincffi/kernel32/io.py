"""
Files
-----

A module containing common Windows file functions.
"""

from collections import namedtuple

from six import integer_types, string_types

from pywincffi.core import dist
from pywincffi.core.checks import Enums, input_check, error_check
from pywincffi.exceptions import WindowsAPIError
from pywincffi.kernel32.handle import INVALID_HANDLE_VALUE


FileTime = namedtuple(
    "FileTime", ("dwLowDateTime", "dwHighDateTime")
)
FileInformation = namedtuple(
    "FileInformation",
    ("dwFileAttributes", "ftCreationTime", "ftLastAccessTime",
     "ftLastWriteTime", "dwVolumeSerialNumber", "nFileSizeHigh",
     "nFileSizeLow", "nNumberOfLinks", "nFileIndexHigh", "nFileIndexLow")
)


def WriteFile(hFile, lpBuffer, lpOverlapped=None):
    """
    Writes data to ``hFile`` which may be an I/O device for file.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365747

    :param handle hFile:
        The handle to write to

    :type lpBuffer: bytes, string or unicode.
    :param lpBuffer:
        The data to be written to the file or device. We should be able
        to convert this value to unicode.

    :type lpOverlapped: None or OVERLAPPED
    :param lpOverlapped:
        None or a pointer to a ``OVERLAPPED`` structure.  See Microsoft's
        documentation for intended usage and below for an example of this
        struct.

        >>> from pywincffi.core import dist
        >>> ffi, library = dist.load()
        >>> hFile = None # normally, this would be a handle
        >>> lpOverlapped = ffi.new(
        ...     "OVERLAPPED[1]", [{
        ...         "hEvent": hFile
        ...     }]
        ... )
        >>> bytes_written = WriteFile(
        ...     hFile, "Hello world", lpOverlapped=lpOverlapped)

    :returns:
        Returns the number of bytes written
    """
    ffi, library = dist.load()

    if lpOverlapped is None:
        lpOverlapped = ffi.NULL

    input_check("hFile", hFile, Enums.HANDLE)
    input_check("lpBuffer", lpBuffer, Enums.UTF8)
    input_check("lpOverlapped", lpOverlapped, Enums.OVERLAPPED)

    # Prepare string and outputs
    nNumberOfBytesToWrite = len(lpBuffer)
    lpBuffer = ffi.new("wchar_t[%d]" % nNumberOfBytesToWrite, lpBuffer)
    bytes_written = ffi.new("LPDWORD")

    code = library.WriteFile(
        hFile, lpBuffer, ffi.sizeof(lpBuffer), bytes_written, lpOverlapped)
    error_check("WriteFile", code=code, expected=Enums.NON_ZERO)

    return bytes_written[0]


def ReadFile(hFile, nNumberOfBytesToRead, lpOverlapped=None):
    """
    Read the specified number of bytes from ``hFile``.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa365467

    :param handle hFile:
        The handle to read from

    :param int nNumberOfBytesToRead:
        The number of bytes to read from ``hFile``

    :param OVERLAPPED lpOverlapped:
        None or a pointer to a ``OVERLAPPED`` structure.  See Microsoft's
        documentation for intended usage and below for an example of this
        struct.

        >>> from pywincffi.core import dist
        >>> ffi, library = dist.load()
        >>> hFile = None # normally, this would be a handle
        >>> lpOverlapped = ffi.new(
        ...     "OVERLAPPED[1]", [{
        ...         "hEvent": hFile
        ...     }]
        ... )
        >>> read_data = ReadFile(  # read 12 bytes from hFile
        ...     hFile, 12, lpOverlapped=lpOverlapped)

    :returns:
        Returns the data read from ``hFile``
    """
    ffi, library = dist.load()

    if lpOverlapped is None:
        lpOverlapped = ffi.NULL

    input_check("hFile", hFile, Enums.HANDLE)
    input_check("nNumberOfBytesToRead", nNumberOfBytesToRead, integer_types)
    input_check("lpOverlapped", lpOverlapped, Enums.OVERLAPPED)

    lpBuffer = ffi.new("wchar_t[%d]" % nNumberOfBytesToRead)
    bytes_read = ffi.new("LPDWORD")
    code = library.ReadFile(
        hFile, lpBuffer, ffi.sizeof(lpBuffer), bytes_read, lpOverlapped
    )
    error_check("ReadFile", code=code, expected=Enums.NON_ZERO)
    return ffi.string(lpBuffer)


def CreateFile(
    lpFileName, dwDesiredAccess=None, dwShareMode=None,
    lpSecurityAttributes=None, dwCreationDisposition=None,
    dwFlagsAndAttributes=None, hTemplateFile=None):
    """
    Creates or opens a file or other I/O device.  See Microsoft's
    documentation below for a more detailed explanation of the input
    arguments.  Most of the defaults are meant to approximate the same
    behavior as Python's :func:`open` function.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa363858

    :param str lpFileName:
        Name of the device or filename to be created or opened.  See
        Microsoft's documentation for more detailed information.

    :keyword int dwDesiredAccess:
        The requested access to the file or device.  By default
        the file will be opened with ``GENERIC_READ`` access.

    :keyword int dwShareMode:
        Controls how you wish to share this file object with other
        processes.  By default the file handle will not be shared with
        other processes.

    :keyword LPSECURITY_ATTRIBUTES lpSecurityAttributes:
        A structure containing information about the security attributes.

    :keyword int dwCreationDisposition:
        What to do when the file or devices exists or not exists.  By default
        this function will create the file or device if it does not exist and
        overwrite it if it does and it's writable.  In Windows terms, this
        is the ``CREATE_ALWAYS`` mode.

    :keyword int dwFlagsAndAttributes:
        Attributes to apply to the file.  By default, no special attributes are
        applied.

    :keyword handle hTemplateFile:
        An optional template handle used to apply file attributes and
        extended attributes to the file being created.  By default, this is
        not used.
    """
    ffi, library = dist.load()

    input_check("lpFileName", lpFileName, string_types)
    lpFileName = ffi.new("wchar_t[%d]" % len(lpFileName), lpFileName)

    if dwDesiredAccess is None:
        dwDesiredAccess = library.GENERIC_READ

    if dwShareMode is None:
        dwShareMode = 0

    if lpSecurityAttributes is None:
        lpSecurityAttributes = ffi.NULL

    if dwCreationDisposition is None:
        dwCreationDisposition = library.CREATE_ALWAYS

    if dwFlagsAndAttributes is None:
        dwFlagsAndAttributes = library.FILE_ATTRIBUTE_NORMAL

    if hTemplateFile is None:
        hTemplateFile = ffi.NULL
    else:
        input_check("hTemplateFile", hTemplateFile, Enums.FILE)

    # Input checks
    input_check("dwDesiredAccess", dwDesiredAccess, integer_types)
    input_check("dwShareMode", dwShareMode, integer_types)
    input_check(
        "lpSecurityAttributes", lpSecurityAttributes,
        Enums.LPSECURITY_ATTRIBUTES)
    input_check("dwCreationDisposition", dwCreationDisposition, integer_types)
    input_check("dwFlagsAndAttributes", dwFlagsAndAttributes, integer_types)

    handle = library.CreateFile(
        ffi.cast("LPCTSTR", lpFileName),
        ffi.cast("DWORD", dwDesiredAccess),
        ffi.cast("DWORD", dwShareMode),
        lpSecurityAttributes,
        ffi.cast("DWORD", dwCreationDisposition),
        ffi.cast("DWORD", dwFlagsAndAttributes),
        hTemplateFile
    )

    if handle == INVALID_HANDLE_VALUE:  # pragma: no cover
        raise WindowsAPIError(
            "CreateFile", ffi.getwinerror()[-1], INVALID_HANDLE_VALUE,
            "not %s" % INVALID_HANDLE_VALUE)

    return handle


def GetFileInformationByHandle(hFile):
    """
    Retrieves information about the specified ``hFile``.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/aa364952

    :param handle hFile:
        The handle to retrieve information for.

    :returns:
        Returns an instance of :class:`FileInformation`
    """
    input_check("hFile", hFile, Enums.HANDLE)

    ffi, library = dist.load()
    lpFileInformation = ffi.new("LPBY_HANDLE_FILE_INFORMATION")
    code = library.GetFileInformationByHandle(hFile, lpFileInformation)
    error_check(
        "GetFileInformationByHandle", code=code, expected=Enums.NON_ZERO)

    return FileInformation(
        dwFileAttributes=lpFileInformation.dwFileAttributes,
        ftCreationTime=FileTime(
            dwLowDateTime=lpFileInformation.ftCreationTime.dwLowDateTime,
            dwHighDateTime=lpFileInformation.ftCreationTime.dwHighDateTime
        ),
        ftLastAccessTime=FileTime(
            dwLowDateTime=lpFileInformation.ftLastAccessTime.dwLowDateTime,
            dwHighDateTime=lpFileInformation.ftLastAccessTime.dwHighDateTime
        ),
        ftLastWriteTime=FileTime(
            dwLowDateTime=lpFileInformation.ftLastWriteTime.dwLowDateTime,
            dwHighDateTime=lpFileInformation.ftLastWriteTime.dwHighDateTime
        ),
        dwVolumeSerialNumber=lpFileInformation.dwVolumeSerialNumber,
        nFileSizeHigh=lpFileInformation.nFileSizeHigh,
        nFileSizeLow=lpFileInformation.nFileSizeLow,
        nNumberOfLinks=lpFileInformation.nNumberOfLinks,
        nFileIndexHigh=lpFileInformation.nFileIndexHigh,
        nFileIndexLow=lpFileInformation.nFileIndexLow
    )
