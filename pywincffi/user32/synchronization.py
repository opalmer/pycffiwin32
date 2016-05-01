"""
Synchronization
---------------

This module contains general functions for synchronizing objects and
events.  The functions provided in this module are parts of the ``user32``
library.

.. seealso::

    :mod:`pywincffi.kernel32.synchronization`
"""

from six import integer_types

from pywincffi.core import dist
from pywincffi.core.checks import input_check
from pywincffi.exceptions import WindowsAPIError


def MsgWaitForMultipleObjects(
        pHandles, bWaitAll, dwMilliseconds, dwWakeMask, nCount=None):
    """
    Waits until one or all of the specified objects are in a singled state
    or the timeout elapses.

    .. seealso::

        https://msdn.microsoft.com/en-us/library/ms684242

    :param list pHandles:
        A list of objects to wait on.  See Microsoft's documentation for
        more information about the contents of this variable.

    :param bool bWaitAll:
        If True then this function will return when the states of all
        objects in ``pHandles`` are signaled.

    :param int dwMilliseconds:
        The timeout interval in milliseconds.

    :param int dwWakeMask:
        The input types for which an input event object handle will be added
        to the array of handles.  See Microsoft's documentation for more
        detailed information.

    :keyword int nCount:
        The number of object handles in ``pHandles``.  By default this will
        be determined by checking the length of the input to ``pHandles``.

    :raises WindowsAPIError:
        Raised if the underlying Windows function returns ``WAIT_FAILED``.

    :rtype: int
    :return:
        Returns the value of the event which caused the function to
        return.  See Microsoft's documentation for full details on what
        this could be.
    """
    if nCount is None:
        nCount = len(pHandles)

    input_check("pHandles", pHandles, (list, tuple))
    input_check("bWaitAll", bWaitAll, bool)
    input_check("dwMilliseconds", dwMilliseconds, integer_types)
    input_check("dwWakeMask", dwWakeMask, integer_types)
    input_check("nCount", nCount, integer_types)

    ffi, library = dist.load()

    code = library.MsgWaitForMultipleObjects(
        nCount,
        pHandles,
        bWaitAll,
        dwMilliseconds,
        dwWakeMask
    )

    if code == library.WAIT_FAILED:
        code, message = ffi.getwinerror()
        raise WindowsAPIError(
            "MsgWaitForMultipleObjects", message, code)

    return code
