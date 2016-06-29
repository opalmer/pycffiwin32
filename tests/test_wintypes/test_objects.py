from pywincffi.core import dist
from pywincffi.dev.testutil import TestCase
from pywincffi.wintypes import HANDLE, SOCKET


class ObjectBaseTestCase(TestCase):
    """
    A base test case which wraps testing of core object
    types.
    """
    OBJECT_CLASS = None

    def setUp(self):
        super(ObjectBaseTestCase, self).setUp()

        if self.__class__ == ObjectBaseTestCase:
            self.skipTest("ObjectBaseTestCase not a real test")

        if self.OBJECT_CLASS is None:
            self.fail("`OBJECT_CLASS` not set")

    def cast_from_value(self, int_data):
        raise NotImplementedError

    def test_instantiate(self):
        h = self.OBJECT_CLASS()  # pylint: disable=not-callable
        self.assertIsInstance(h, self.OBJECT_CLASS)

    def test_compare_equal_highlevel(self):
        h1 = self.OBJECT_CLASS()  # pylint: disable=not-callable
        h2 = self.OBJECT_CLASS()  # pylint: disable=not-callable
        self.assertIsNot(h1, h2)
        self.assertEqual(h1, h2)

    def test_compare_equal_lowlevel(self):
        h1 = self.cast_from_value(42)
        h2 = self.cast_from_value(42)
        self.assertIsNot(h1, h2)
        self.assertEqual(h1, h2)

    def test_compare_different_lowlevel(self):
        h1 = self.cast_from_value(42)
        h2 = self.cast_from_value(43)
        self.assertIsNot(h1, h2)
        self.assertNotEqual(h1, h2)

    def test_compare_wrong_type(self):
        h = self.OBJECT_CLASS()  # pylint: disable=not-callable
        with self.assertRaises(TypeError):
            if h == 0:
                pass


class TestHANDLE(ObjectBaseTestCase):
    """
    Tests for :class:`pywincffi.wintypes.HANDLE`
    """
    OBJECT_CLASS = HANDLE

    def cast_from_value(self, int_data):
        ffi, _ = dist.load()
        cdata = ffi.new(self.OBJECT_CLASS.C_TYPE)
        cdata[0] = ffi.cast(self.OBJECT_CLASS.__name__, int_data)
        return self.OBJECT_CLASS(cdata[0])


class TestSOCKET(ObjectBaseTestCase):
    """
    Tests for :class:`pywincffi.wintypes.SOCKET`
    """
    OBJECT_CLASS = SOCKET

    def cast_from_value(self, int_data):
        ffi, _ = dist.load()
        s = self.OBJECT_CLASS()
        s._cdata[0] = ffi.cast("SOCKET", int_data)
        return s
