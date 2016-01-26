from pywincffi.dev.testutil import TestCase
from pywincffi.kernel32.io import WriteFile, ReadFile


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
