import os

from pywincffi.core.ffi import Library
from pywincffi.core.testutil import TestCase
from pywincffi.exceptions import WindowsAPIError
from pywincffi.kernel32.io import CreatePipe, CloseHandle
from pywincffi.kernel32.process import (
    OpenProcess, GetCurrentProcess, GetCurrentProcessId, GetProcessId,
    DuplicateHandle)


class TestOpenProcess(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.process.OpenProcess`
    """
    def test_returns_handle(self):
        ffi, library = Library.load()

        handle = OpenProcess(
            library.PROCESS_QUERY_LIMITED_INFORMATION,
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
        ffi, library = Library.load()

        current_process = GetCurrentProcess()
        typeof = ffi.typeof(current_process)
        self.assertEqual(typeof.kind, "pointer")
        self.assertEqual(typeof.cname, "void *")

    def test_get_current_process_pid_by_handle(self):
        current_process = GetCurrentProcess()
        self.assertEqual(GetProcessId(current_process), os.getpid())

    def test_get_current_process_pid(self):
        self.assertEqual(GetCurrentProcessId(), os.getpid())


class TestDuplicateHandle(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.process.DuplicateHandle`
    """
    def test_duplicate_write_pipe_result_type(self):
        ffi, library = Library.load()

        reader, writer = CreatePipe()
        self.addCleanup(CloseHandle, reader)
        self.addCleanup(CloseHandle, writer)
        current_process = GetCurrentProcess()
        result = DuplicateHandle(
            current_process,
            writer,
            current_process,
            library.DUPLICATE_SAME_ACCESS,
            False
        )
        typeof = ffi.typeof(result)
        self.assertEqual(typeof.kind, "pointer")
        self.assertEqual(typeof.cname, "void * *")

    # TODO: test more than than just the return type
    # TODO: test_duplicate_read_pipe



