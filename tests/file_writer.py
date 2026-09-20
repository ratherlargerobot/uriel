import os
import gzip
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

    def test_missing_dest_directory(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            missing_dir = os.path.join(tmp_dir, "does-not-exist")
            file_path = os.path.join(missing_dir, "test")

            try:
                uriel.FileWriter(file_path)
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "could not create file '%s', because directory " %
                    (file_path) +
                    "'%s' does not exist" % (missing_dir),
                    str(e))

    def test_file_not_found_with_dest_directory_that_exists(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            missing_src = os.path.join(tmp_dir, "does-not-exist", "target")
            file_path = os.path.join(tmp_dir, "test")

            os.symlink(missing_src, file_path)

            self.assertRaises(uriel.UrielError, uriel.FileWriter, file_path)


class TestGzipFileWriter(unittest.TestCase):
    """
    Tests the GzipFileWriter class.

    """

    def test_write_text_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            file_path = os.path.join(tmp_dir, "test.gz")
            file_writer = uriel.GzipFileWriter(file_path)
            file_writer.write("foo\nbar\n")
            file_writer.close()

            self.assertTrue(os.path.exists(file_path))

            data = None
            with gzip.open(file_path, "rt") as f:
                data = f.read()
            self.assertEqual("foo\nbar\n", data)

    def test_missing_dest_directory(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            missing_dir = os.path.join(tmp_dir, "does-not-exist")
            file_path = os.path.join(missing_dir, "test.gz")

            try:
                uriel.GzipFileWriter(file_path)
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "could not create file '%s', because directory " %
                    (file_path) +
                    "'%s' does not exist" % (missing_dir),
                    str(e))

    def test_file_not_found_with_dest_directory_that_exists(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            missing_src = os.path.join(tmp_dir, "does-not-exist", "target")
            file_path = os.path.join(tmp_dir, "test.gz")

            os.symlink(missing_src, file_path)

            self.assertRaises(uriel.UrielError,
                              uriel.GzipFileWriter,
                              file_path)

