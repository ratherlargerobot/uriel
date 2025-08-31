import os
import unittest

from .util import UrielContainer
from .util import TempDir

class TestFileWriter(unittest.TestCase):
    """
    Tests the FileWriter class.

    """

    def test_write_empty_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            file_path = os.path.join(tmp_dir, "test")
            file_writer = uriel.FileWriter(file_path)
            file_writer.close()

            self.assertTrue(os.path.exists(file_path))
            self.assertEqual(0, os.path.getsize(file_path))

    def test_write_text_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            file_path = os.path.join(tmp_dir, "test")
            file_writer = uriel.FileWriter(file_path)
            file_writer.write("foo\nbar\n")
            file_writer.close()

            self.assertTrue(os.path.exists(file_path))
            self.assertEqual(8, os.path.getsize(file_path))

            data = None
            with open(file_path, "r") as f:
                data = f.read()
            self.assertEqual("foo\nbar\n", data)

    def test_write_binary_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            file_path = os.path.join(tmp_dir, "test")
            file_writer = uriel.FileWriter(file_path, mode="wb")
            file_writer.write(bytes([0x00, 0xFF]))
            file_writer.close()

            self.assertTrue(os.path.exists(file_path))
            self.assertEqual(2, os.path.getsize(file_path))

            data = None
            with open(file_path, "rb") as f:
                data = f.read()
            self.assertEqual(bytes([0x00, 0xFF]), data)

