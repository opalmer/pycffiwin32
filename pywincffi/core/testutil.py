"""
Test Utility
------------

This module is used by the unittests.
"""

import atexit
import os
import shutil
import tempfile
from errno import ENOENT, EACCES, EAGAIN, EIO
from os.path import isfile, isdir

from cffi import FFI, CDefError

try:
    # The setup.py file installs unittest2 for Python 2
    # which backports newer test framework features.
    from unittest2 import TestCase as _TestCase
except ImportError:
    # pylint: disable=wrong-import-order
    from unittest import TestCase as _TestCase

from pywincffi.core.config import config
from pywincffi.core.logger import get_logger

logger = get_logger("core.testutil")

# To keep lint on non-windows platforms happy.
try:
    WindowsError
except NameError:
    WindowsError = OSError  # pylint: disable=redefined-builtin

# Load in our own kernel32 with the function(s) we need
# so we don't have to rely on pywincffi.core
libtest = None  # pylint: disable=invalid-name
ffi = FFI()

try:
    ffi.cdef("void SetLastError(DWORD);")
    libtest = ffi.dlopen("kernel32")  # pylint: disable=invalid-name
except (AttributeError, OSError, CDefError):
    if os.name == "nt":
        logger.warning("Failed to build SetLastError()")


class TestCase(_TestCase):
    """
    A base class for all test cases.  By default the
    core test case just provides some extra functionality.
    """
    def setUp(self):
        if os.name == "nt":
            # Always reset the last error to 0 between tests.  This
            # ensures that any error we intentionally throw in one
            # test does not causes an error to be raised in another.
            self.SetLastError(0)

        config.load()

    # pylint: disable=invalid-name
    def SetLastError(self, value=0, lib=None):
        """Calls the Windows API function SetLastError()"""
        self.failIf(os.name != "nt")

        if lib is None:
            lib = libtest

        if lib is None:
            self.fail("`lib` was not defined")

        if not isinstance(value, int):
            self.fail("Expected int for `value`")

        return lib.SetLastError(ffi.cast("DWORD", value))
