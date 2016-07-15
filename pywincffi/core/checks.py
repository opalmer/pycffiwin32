"""
Checks
======

Provides functions that are responsible for internal type checks.
"""

import enum
from six import string_types

from pywincffi.core import dist
from pywincffi.exceptions import WindowsAPIError, InputError

NoneType = type(None)
Enums = enum.Enum("Enums", """
NON_ZERO
""".strip())


def error_check(function, code=None, expected=None):
    """
    Checks the results of a return code against an expected result.  If
    a code is not provided we'll use :func:`ffi.getwinerror` to retrieve
    the code.

    :param str function:
        The Windows API function being called.

    :keyword int code:
        An explicit code to compare against.

    :keyword int expected:
        The code we expect to have as a result of a successful
        call.  This can also be passed ``pywincffi.core.checks.Enums.NON_ZERO``
        if ``code`` can be anything but zero.

    :raises pywincffi.exceptions.WindowsAPIError:
        Raised if we receive an unexpected result from a Windows API call
    """
    ffi, _ = dist.load()
    errno, error_message = ffi.getwinerror()

    if code is not None:
        if expected == Enums.NON_ZERO and code == 0:
            raise WindowsAPIError(
                function, error_message, errno,
                return_code=code, expected_return_code=expected)
        return

    if errno != 0:
        raise WindowsAPIError(
            function, error_message, errno, return_code=code,
            expected_return_code=expected)


def input_check(name, value, allowed_types=None, allowed_values=None):
    """
    A small wrapper around :func:`isinstance`.  This is mainly meant
    to be used inside of other functions to pre-validate input rater
    than using assertions.  It's better to fail early with bad input
    so more reasonable error message can be provided instead of from
    somewhere deep in cffi or Windows.

    :param str name:
        The name of the input being checked.  This is provided
        so error messages make more sense and can be attributed
        to specific input arguments.

    :param value:
        The value we're performing the type check on.

    :keyword allowed_types:
        The allowed type or types for ``value``.  This argument
        also supports a special value, ``pywincffi.core.checks.Enums.HANDLE``,
        which will check to ensure ``value`` is a handle object.

    :keyword tuple allowed_values:
        A tuple of allowed values.  When provided ``value`` must
        be in this tuple otherwise :class:`InputError` will be
        raised.

    :raises pywincffi.exceptions.InputError:
        Raised if ``value`` is not an instance of ``allowed_types``
    """
    assert isinstance(name, string_types)
    assert allowed_values is None or isinstance(allowed_values, tuple)
    ffi, _ = dist.load()

    if allowed_types is None and isinstance(allowed_values, tuple):
        if value not in allowed_values:
            raise InputError(
                name, value, allowed_types,
                allowed_values=allowed_values, ffi=ffi)

    else:
        if not isinstance(value, allowed_types):
            raise InputError(name, value, allowed_types, ffi=ffi)
