try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from pywincffi.core.testutil import TestCase
from pywincffi.exceptions import WindowsAPIError
from pywincffi.kernel32.io import CreatePipe, CloseHandle, WriteFile, ReadFile


class CreatePipeTest(TestCase):
    """
    Basic tests for :func:`pywincffi.files.CreatePipe` and
    :func:`pywincffi.files.CloseHandle`
    """
    def test_create_and_close_pipes(self):
        reader, writer = CreatePipe()

        CloseHandle(writer)

        # Second attempt should fail
        with self.assertRaises(WindowsAPIError):
            CloseHandle(writer)

        # Second attempt should fail
        CloseHandle(reader)
        with self.assertRaises(WindowsAPIError):
            CloseHandle(reader)


class AnonymousPipeReadWriteTest(TestCase):
    """
    Basic tests for :func:`pywincffi.files.WritePipe` and
    :func:`pywincffi.files.ReadPipe`
    """
    def test_bytes_written(self):
        reader, writer = CreatePipe()
        self.addCleanup(CloseHandle, reader)
        self.addCleanup(CloseHandle, writer)

        data = b"hello world".decode("utf-8")
        bytes_written = WriteFile(writer, data)
        self.assertEqual(bytes_written, len(data) * 2)

    def test_bytes_read(self):
        reader, writer = CreatePipe()
        self.addCleanup(CloseHandle, reader)
        self.addCleanup(CloseHandle, writer)

        data = b"hello world".decode("utf-8")
        data_written = WriteFile(writer, data)

        read_data = ReadFile(reader, data_written)
        self.assertEqual(data, read_data)

    def test_partial_bytes_read(self):
        reader, writer = CreatePipe()
        self.addCleanup(CloseHandle, reader)
        self.addCleanup(CloseHandle, writer)

        data = b"hello world".decode("utf-8")
        WriteFile(writer, data)

        read_data = ReadFile(reader, 5)
        self.assertEqual(read_data, "hello")

        read_data = ReadFile(reader, 6)
        self.assertEqual(read_data, " world")

    def test_read_more_bytes_than_written(self):
        reader, writer = CreatePipe()
        self.addCleanup(CloseHandle, reader)
        self.addCleanup(CloseHandle, writer)

        data = b"hello world".decode("utf-8")
        data_written = WriteFile(writer, data)

        read_data = ReadFile(reader, data_written * 2)
        self.assertEqual(data, read_data)


class TestSetNamedPipeHandleState(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.io.SetNamedPipeHandleState` and
    :func:`pywincffi.kernel32.io.GetNamedPipeHandleState`
    """
