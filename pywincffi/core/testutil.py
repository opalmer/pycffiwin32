"""
Test Utility
------------

This module is used by the unittests.
"""

import atexit
import os
import shutil
import sys
import tempfile
from errno import ENOENT, EACCES, EAGAIN, EIO
from os.path import isfile, isdir

from cffi import FFI

if sys.version_info[0:2] != (2, 6):
    # pylint: disable=wrong-import-order
    from unittest import TestCase as _TestCase
else:
    from unittest2 import TestCase as _TestCase

# To keep lint on non-windows platforms happy.
try:
    WindowsError
except NameError:
    WindowsError = OSError  # pylint: disable=redefined-builtin

# Load in our own kernel32 with the function(s) we need
# so we don't have to rely on pywincffi.core
kernel32 = None
if not os.environ.get("READTHEDOCS"):
    ffi = FFI()
    ffi.cdef("void SetLastError(DWORD);")
    kernel32 = ffi.dlopen("kernel32")


def remove(path, onexit=True):
    """
    Removes the request ``path`` from disk.  This is meant to
    be used as a cleanup function by a test case.

    :param str path:
        The file or directory to remove.

    :param bool onexit:
        If we can't remove the request ``path``, try again
        when Python exists to remove it.
    """
    if isdir(path):
        try:
            shutil.rmtree(path)
        except (WindowsError, OSError, IOError) as error:
            if error.errno == ENOENT:
                return
            if error.errno in (EACCES, EAGAIN, EIO) and onexit:
                atexit.register(remove, path, onexit=False)

    elif isfile(path):
        try:
            os.remove(path)
        except (WindowsError, OSError, IOError) as error:
            if error.errno == ENOENT:
                return
            if error.errno in (EACCES, EAGAIN, EIO) and onexit:
                atexit.register(remove, path, onexit=False)


class TestCase(_TestCase):
    """
    A base class for all test cases.  By default the
    core test case just provides some extra functionality.
    """
    def setUp(self):
        if kernel32 is None:
            self.fail("kernel32 was never defined")

        # Always reset the last error to 0 between tests.  This
        # ensures that any error we intentionally throw in one
        # test does not causes an error to be raised in another.
        kernel32.SetLastError(ffi.cast("DWORD", 0))

    def tempdir(self):
        """
        Creates a temporary directory and returns the path.  Best attempts
        will be made to cleanup the directory at the end of the test run.
        """
        path = tempfile.mkdtemp()
        self.addCleanup(remove, path)
        return path

    def tempfile(self, data=None):
        """
        Creates a temporary file and returns the path.  Best attempts
        will be made to cleanup the file at the end of the test run.

        :param str data:
            Optionally write the provided data to the file on disk.
        """
        fd, path = tempfile.mkstemp()
        if data is None:
            os.close(fd)
        else:
            with os.fdopen(fd, "w") as file_:
                file_.write(data)

        self.addCleanup(remove, path)
        return path
