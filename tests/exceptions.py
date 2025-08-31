import unittest

from .util import UrielContainer

class TestUrielError(unittest.TestCase):
    """
    Tests the UrielError class.

    """

    def test_is_exception_subclass(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.UrielError()
        self.assertTrue(issubclass(type(e), Exception))

    def test_no_arg_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.UrielError()
        self.assertEqual("", str(e))

    def test_string_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.UrielError("foo")
        self.assertEqual("foo", str(e))


class TestSojuError(unittest.TestCase):
    """
    Tests the SojuError class.

    """

    def test_is_exception_subclass(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.SojuError()
        self.assertTrue(issubclass(type(e), Exception))

    def test_no_arg_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.SojuError()
        self.assertEqual("", str(e))

    def test_string_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.SojuError("foo")
        self.assertEqual("foo", str(e))


class TestHandlerError(unittest.TestCase):
    """
    Tests the HandlerError class.

    """

    def test_is_exception_subclass(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.HandlerError()
        self.assertTrue(issubclass(type(e), Exception))

    def test_no_arg_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.HandlerError()
        self.assertEqual("", str(e))

    def test_string_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.HandlerError("foo")
        self.assertEqual("foo", str(e))

