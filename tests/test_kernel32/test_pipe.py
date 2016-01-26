from random import randint
from pywincffi.core import dist
from pywincffi.dev.testutil import TestCase
from pywincffi.exceptions import WindowsAPIError
from pywincffi.kernel32.handle import CloseHandle, handle_from_file
from pywincffi.kernel32.io import WriteFile, ReadFile
from pywincffi.kernel32.pipe import (
    PeekNamedPipeResult, CreatePipe, PeekNamedPipe, SetNamedPipeHandleState,
    GetNamedPipeHandleState, GetNamedPipeInfo, NamedPipeInfo)


class CreatePipeTest(TestCase):
    """
    Basic tests for :func:`pywincffi.kernel32.pipe.CreatePipe` and
    :func:`pywincffi.kernel32.pipe.CloseHandle`
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


# TODO: tests for lpBuffer from the result
class TestPeekNamedPipe(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.pipe.PeekNamedPipe`.
    """
    def test_return_type(self):
        reader, _ = self.create_anonymous_pipes()
        self.assertIsInstance(PeekNamedPipe(reader, 0), PeekNamedPipeResult)

    def test_peek_does_not_remove_data(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        data_written = WriteFile(writer, data)

        PeekNamedPipe(reader, 0)
        self.assertEqual(ReadFile(reader, data_written), data)

    def test_bytes_read_less_than_bytes_written(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        WriteFile(writer, data)

        result = PeekNamedPipe(reader, 1)
        self.assertEqual(result.lpBytesRead, 1)

    def test_bytes_read_greater_than_bytes_written(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        bytes_written = WriteFile(writer, data)

        result = PeekNamedPipe(reader, bytes_written * 2)
        self.assertEqual(result.lpBytesRead, bytes_written)

    def test_total_bytes_avail(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        bytes_written = WriteFile(writer, data)

        result = PeekNamedPipe(reader, 0)
        self.assertEqual(result.lpTotalBytesAvail, bytes_written)

    def test_total_bytes_avail_after_read(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        bytes_written = WriteFile(writer, data)

        read_bytes = 7
        ReadFile(reader, read_bytes)

        result = PeekNamedPipe(reader, 0)
        self.assertEqual(
            result.lpTotalBytesAvail, bytes_written - (read_bytes * 2))


class TestSetNamedPipeHandleState(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.pipe.SetNamedPipeHandleState`
    """
    def test_sets_lpMode(self):
        ffi, library = dist.load()
        reader, writer = self.create_anonymous_pipes()
        SetNamedPipeHandleState(
            reader, lpMode=library.PIPE_READMODE_BYTE | library.PIPE_NOWAIT
        )
        info = GetNamedPipeInfo(reader)
        self.assertEqual(
            info.lpFlags, library.PIPE_READMODE_BYTE | library.PIPE_NOWAIT
        )

    # TODO: try CreateFile() with a named pipe, lpMaxCollectionCount has
    # some restrictions
    def test_sets_lpMaxCollectionCount(self):
        pass
        # ffi, library = dist.load()
        # reader, writer = self.create_anonymous_pipes(nSize=128)
        # # for handle in self.create_anonymous_pipes(nSize=128):
        # count = randint(2, 20)
        #
        # import tempfile, os
        # fd, path = tempfile.mkstemp()
        # with os.fdopen(fd, "w") as file_:
        #     handle = handle_from_file(file_)
        #
        #     # SetNamedPipeHandleState(handle, lpMaxCollectionCount=3)
        #     # info = GetNamedPipeInfo(handle)
        #     # self.assertEqual(
        #     #     info.lpMaxCollectionCount, count
        #     # )


class TestGetNamedPipeInfo(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.pipe.GetNamedPipeInfo`
    """
    def test_return_type(self):
        reader, _ = self.create_anonymous_pipes()
        info = GetNamedPipeInfo(reader)
        self.assertIsInstance(info, NamedPipeInfo)

    def test_lpFlags(self):
        ffi, library = dist.load()
        reader, writer = self.create_anonymous_pipes()
        reader_info = GetNamedPipeInfo(reader)
        writer_info = GetNamedPipeInfo(writer)
        self.assertEqual(reader_info.lpFlags, library.PIPE_SERVER_END)
        self.assertEqual(writer_info.lpFlags, library.PIPE_CLIENT_END)

    def test_lpOutBufferSize(self):
        for handle in self.create_anonymous_pipes(nSize=128):
            info = GetNamedPipeInfo(handle)
            self.assertEqual(info.lpOutBufferSize, 128)

    def test_lpInBufferSize(self):
        for handle in self.create_anonymous_pipes(nSize=128):
            info = GetNamedPipeInfo(handle)
            self.assertEqual(info.lpInBufferSize, 128)

    # TODO: try CreateFile() with a named pipe, lpMaxCollectionCount has
    # some restrictions
    def test_lpMaxInstances(self):
        pass
        # for handle in self.create_anonymous_pipes():
        #     count = randint(1, 20)
        #     SetNamedPipeHandleState(handle, lpMaxCollectionCount=count)
        #     info = GetNamedPipeInfo(handle)
        #     self.assertEqual(info.lpMaxInstances, count)



