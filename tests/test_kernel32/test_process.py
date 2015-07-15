import os

from pywincffi.core.ffi import ffi
from pywincffi.core.testutil import TestCase
from pywincffi.exceptions import WindowsAPIError
from pywincffi.kernel32.process import (
    PROCESS_QUERY_LIMITED_INFORMATION, OpenProcess, GetCurrentProcess,
    GetProcessId, GetCurrentProcessId)


class TestOpenProcess(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.process.OpenProcess`
    """
    def test_returns_handle(self):
        handle = OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION,
            False,
            os.getpid()
        )
        typeof = ffi.typeof(handle)
        self.assertEqual(typeof.kind, "pointer")
        self.assertEqual(typeof.cname, "void *")

    def test_access_denied_for_null_desired_access(self):
        with self.assertRaises(WindowsAPIError) as error:
            OpenProcess(0, False, os.getpid())

        self.assertEqual(error.exception.code, 5)


class TestGetProcess(TestCase):
    """
    Tests for pywincffi.kernel32.process.GetProcess* functions
    """
    def test_get_current_process_type(self):
        current_process = GetCurrentProcess()
        typeof = ffi.typeof(current_process)
        self.assertEqual(typeof.kind, "pointer")
        self.assertEqual(typeof.cname, "void *")

    def test_get_current_process_pid_by_handle(self):
        current_process = GetCurrentProcess()
        self.assertEqual(GetProcessId(current_process), os.getpid())

    def test_get_current_process_pid(self):
        self.assertEqual(GetCurrentProcessId(), os.getpid())


