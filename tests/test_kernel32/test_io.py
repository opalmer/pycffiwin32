import shutil
import tempfile
import os
from random import choice
from string import ascii_letters
from os.path import join, isfile

from pywincffi.core import dist
from pywincffi.dev.testutil import TestCase
from pywincffi.kernel32.handle import CloseHandle
from pywincffi.kernel32.io import (
    WriteFile, ReadFile, CreateFile, GetFileInformationByHandle)


class AnonymousPipeReadWriteTest(TestCase):
    """
    Basic tests for :func:`pywincffi.kernel32.io.WriteFile` and
    :func:`pywincffi.kernel32.io.ReadFile`
    """
    def test_bytes_written(self):
        _, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        bytes_written = WriteFile(writer, data)
        self.assertEqual(bytes_written, len(data) * 2)

    def test_bytes_read(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        data_written = WriteFile(writer, data)

        read_data = ReadFile(reader, data_written)
        self.assertEqual(data, read_data)

    def test_partial_bytes_read(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        WriteFile(writer, data)

        read_data = ReadFile(reader, 5)
        self.assertEqual(read_data, "hello")

        read_data = ReadFile(reader, 6)
        self.assertEqual(read_data, " world")

    def test_read_more_bytes_than_written(self):
        reader, writer = self.create_anonymous_pipes()

        data = b"hello world".decode("utf-8")
        data_written = WriteFile(writer, data)

        read_data = ReadFile(reader, data_written * 2)
        self.assertEqual(data, read_data)


class CreateFileTest(TestCase):
    """
    Tests for :func:`pywincffi.kernel32.io.CreateFile`
    """
    def create_file(self, **kwargs):
        cleanup_dir = kwargs.pop("cleanup_dir", True)
        close_on_exit = kwargs.pop("close_on_exit", True)

        tempdir = tempfile.mkdtemp()
        if cleanup_dir:
            self.addCleanup(shutil.rmtree, tempdir, ignore_errors=True)

        # TODO: duh..convert filename, it cannot contain ":".  Otherwise we get
        # 'The filename, directory name, or volume label syntax is incorrect'
        filename = join(
            tempdir,
            "".join(choice(ascii_letters) for _ in range(10))) + ".txt"

        handle = CreateFile(filename, **kwargs)

        if close_on_exit:
            self.addCleanup(CloseHandle, handle)

        return filename, handle

    def test_creates_file(self):
        path, handle = self.create_file()
        self.assertTrue(isfile(path))
