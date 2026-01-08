import os
import sys
import time
import datetime
import unittest

from .util import UrielContainer
from .util import TempDir

# N.B. we are intentionally skipping tests for the following functions,
#      because they are very simple, and primarly rely on OS interactions:
#
#    sys_exit()
#    log()
#    main()

class TestFunctionWarn(unittest.TestCase):
    """
    Tests the warn() function.

    """

    def test_basic_string(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.warn("foo bar")
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: foo bar", c.stderr[0])
        self.assertIsNone(c.exit_code)

    def test_empty_string(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.warn("")
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: ", c.stderr[0])
        self.assertIsNone(c.exit_code)

    def test_multi_line_string(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.warn("foo\nbar")
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: foo\nbar", c.stderr[0])
        self.assertIsNone(c.exit_code)

    def test_number(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.warn(42)
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: 42", c.stderr[0])
        self.assertIsNone(c.exit_code)

    def test_none(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.warn(None)
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: None", c.stderr[0])
        self.assertIsNone(c.exit_code)


class TestFunctionDie(unittest.TestCase):
    """
    Tests the die() function.

    """

    def test_exit_code_before_calling(self):
        c = UrielContainer()
        uriel = c.uriel

        self.assertIsNone(c.exit_code)

    def test_basic_string(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.die("foo bar")
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: foo bar", c.stderr[0])
        self.assertEqual(1, c.exit_code)

    def test_empty_string(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.die("")
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: ", c.stderr[0])
        self.assertEqual(1, c.exit_code)

    def test_multi_line_string(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.die("foo\nbar")
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: foo\nbar", c.stderr[0])
        self.assertEqual(1, c.exit_code)

    def test_number(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.die(42)
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: 42", c.stderr[0])
        self.assertEqual(1, c.exit_code)

    def test_none(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.die(None)
        self.assertEqual(1, len(c.stderr))
        self.assertEqual("uriel: None", c.stderr[0])
        self.assertEqual(1, c.exit_code)


class TestPrintImpossibleError(unittest.TestCase):
    """
    Tests the print_impossible_error() function.

    """

    def test_print_impossible_error(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.print_impossible_error()
        self.assertEqual(9, len(c.stderr))
        self.assertEqual("uriel: -----------------------------------------------------------------------", c.stderr[0])
        self.assertEqual("uriel: CONGRATULATIONS!", c.stderr[1])
        self.assertEqual("uriel: ", c.stderr[2])
        self.assertEqual("uriel: You found a bug in the uriel program!", c.stderr[3])
        self.assertEqual("uriel: ", c.stderr[4])
        self.assertEqual("uriel: Please consider reporting it, so it can be fixed.", c.stderr[5])
        self.assertEqual("uriel: ", c.stderr[6])
        self.assertEqual("uriel: Sorry for the inconvenience.", c.stderr[7])
        self.assertEqual("uriel: -----------------------------------------------------------------------", c.stderr[8])


class TestFunctionShowUsage(unittest.TestCase):
    """
    Tests the show_usage() function.

    """

    def test_show_usage(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.show_usage()
        self.assertEqual(2, len(c.stderr))
        self.assertEqual("uriel: Yet Another Static Site Generator", c.stderr[0])
        self.assertEqual("Usage: uriel <project-root>", c.stderr[1])
        self.assertEqual(1, c.exit_code)


class TestFunctionPrintablePath(unittest.TestCase):
    """
    Tests the printable_path() function.

    """

    def test_none(self):
        c = UrielContainer()
        uriel = c.uriel

        self.assertRaises(Exception, uriel.printable_path, None)

    def test_empty_string(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = ""
        expected = ""
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)

    def test_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = "/"
        expected = "/"
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)

    def test_leading_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = "/foo"
        expected = "/foo"
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)

    def test_leading_dot_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = "./test/static"
        expected = "test/static"
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)

    def test_multiple_slashes(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = "test///static"
        expected = "test/static"
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)

    def test_trailing_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = "test/static/"
        expected = "test/static"
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)

    def test_multiple_trailing_slashes(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = "test/static///"
        expected = "test/static"
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)

    def test_messy_path(self):
        c = UrielContainer()
        uriel = c.uriel

        input_path = ".///test///static///"
        expected = "test/static"
        actual = uriel.printable_path(input_path)
        self.assertEqual(expected, actual)


class TestFunctionIndentSpaces(unittest.TestCase):
    """
    Tests the indent_spaces() function.

    """

    def test_none(self):
        c = UrielContainer()
        uriel = c.uriel

        self.assertRaises(Exception, uriel.indent_spaces, None)

    def test_negative(self):
        c = UrielContainer()
        uriel = c.uriel

        s = uriel.indent_spaces(-1)
        self.assertEqual("", s)

    def test_zero(self):
        c = UrielContainer()
        uriel = c.uriel

        s = uriel.indent_spaces(0)
        self.assertEqual("", s)

    def test_one_indent(self):
        c = UrielContainer()
        uriel = c.uriel

        s = uriel.indent_spaces(1)
        self.assertEqual("  ", s)

    def test_two_indents(self):
        c = UrielContainer()
        uriel = c.uriel

        s = uriel.indent_spaces(2)
        self.assertEqual("    ", s)

    def test_four_indents(self):
        c = UrielContainer()
        uriel = c.uriel

        s = uriel.indent_spaces(4)
        self.assertEqual("        ", s)


class TestFunctionGetExceptionReason(unittest.TestCase):
    """
    Tests the get_exception_reason() function.

    """

    def test_no_arg_exception(self):
        c = UrielContainer()
        uriel = c.uriel

        e = Exception()

        reason = uriel.get_exception_reason(e)
        self.assertEqual("Exception", reason)

    def test_one_arg_exception(self):
        c = UrielContainer()
        uriel = c.uriel

        e = Exception("foo")

        reason = uriel.get_exception_reason(e)
        self.assertEqual("foo", reason)

    def test_no_arg_uriel_error(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.UrielError()

        reason = uriel.get_exception_reason(e)
        self.assertEqual("UrielError", reason)

    def test_one_arg_uriel_error(self):
        c = UrielContainer()
        uriel = c.uriel

        e = uriel.UrielError("foo")

        reason = uriel.get_exception_reason(e)
        self.assertEqual("foo", reason)


class TestLogFilteredTraceback(unittest.TestCase):
    """
    Tests the log_filtered_traceback() function.

    """

    # N.B. this whole test is somewhat contrived, as it behaves a bit
    #      differently than the code under test normally does.
    #
    # we are filtering tracebacks here, printing them to stderr,
    # but only after a filter_string appears in a line in the traceback.
    #
    # in real code, the filter string is something like "soju.py",
    # where we know the expected project structure, and the filter_string
    # is the entry point into the user-defined code.
    #
    # here, we're running in a unit test, without any user-defined code.
    # so instead, we raise a chained exception, and filter on another
    # somewhat arbitrary string based on the method names.
    #
    # this still exercises the code, but the usage is a bit different.

    # N.B. each line of a traceback contains a \n, so it's actually two lines
    #      first is the file, then a newline, then the error from the file

    def raise_e1(self):
        raise Exception()

    def raise_e2(self, e1):
        raise Exception() from e1

    def test_log_filtered_traceback(self):
        c = UrielContainer()
        uriel = c.uriel

        """

        UNFILTERED TRACEBACK EXAMPLE (3 lines):

Traceback (most recent call last):
  File "/path/to/uriel/tests/uriel_functions.py", line 358, in test_log_filtered_traceback
    self.raise_e2(e1)
  File "/path/to/uriel/tests/uriel_functions.py", line 346, in raise_e2
    raise Exception() from e1


        FILTERED TRACEBACK EXAMPLE (filtered on "in raise_e2", 2 lines):

Traceback (most recent call last):
  File "/path/to/uriel/tests/uriel_functions.py", line 349, in raise_e2
    raise Exception() from e1

        """

        # capture the chained exception, so we can log it
        chained_exception = None

        # create the chained exception
        # we only call helper methods here so that the method names will show
        # up as strings we can filter on for the test
        try:
            try:
                self.raise_e1()
            except Exception as e1:
                self.raise_e2(e1)
        except Exception as e2:
            chained_exception = e2

        # log the filtered traceback to the uriel container stderr
        uriel.log_filtered_traceback(chained_exception, "in raise_e2")

        # since this is a filtered traceback, we expect 2 lines
        self.assertEqual(2, len(c.stderr))

        # the first line is the traceback header message
        self.assertEqual("Traceback (most recent call last):", c.stderr[0])

        # the second line is the filtered part of the traceback message
        # N.B. each traceback line has a \n and prints as two lines
        self.assertTrue(", in raise_e2" in c.stderr[1])
        self.assertTrue("    raise Exception() from e1" in c.stderr[1])


class TestFunctionCopyFile(unittest.TestCase):
    """
    Tests the copy_file() function.

    """

    def test_simple_copy(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_file(src_file, dest_file)

            data = None
            with open(dest_file, "r") as f:
                data = f.read()

            self.assertEqual(3, len(data))
            self.assertEqual("foo", data)

    def test_missing_src_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file,
                              src_file, dest_file)

    def test_src_symlink_dest_missing(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            os.symlink(src_file, src_file)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file,
                              src_file, dest_file)

    def test_src_file_dest_symlink(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            os.symlink(dest_file, dest_file)

            uriel.copy_file(src_file, dest_file)

            data = None
            with open(dest_file, "r") as f:
                data = f.read()

            self.assertFalse(os.path.islink(dest_file))
            self.assertEqual(3, len(data))
            self.assertEqual("foo", data)

    def test_src_symlink_dest_symlink(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            os.symlink(src_file, src_file)
            os.symlink(dest_file, dest_file)

            uriel.copy_file(src_file, dest_file)

            self.assertTrue(os.path.islink(dest_file))
            self.assertEqual(src_file, os.readlink(dest_file))

    def test_src_file_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            os.mkdir(dest_dir)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file,
                              src_file, dest_dir)

    def test_src_dir_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file,
                              src_dir, dest_dir)

    def test_src_dir_dest_missing(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_file = os.path.join(tmp_dir, "dest_file")

            os.mkdir(src_dir)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file,
                              src_dir, dest_file)

    def test_src_permission_error(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            os.chmod(src_file, 0)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file,
                              src_file, dest_file)

    def test_dest_permission_error(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            with open(dest_file, "w") as f:
                f.close()

            os.chmod(dest_file, 0)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file,
                              src_file, dest_file)

    def test_preserve_file_permissions(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            # an unlikely default mode
            os.chmod(src_file, 0o714)

            uriel.copy_file(src_file, dest_file)

            st = os.stat(dest_file)

            self.assertEqual("714", oct(st.st_mode)[-3:])

    def test_preserve_file_times(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_file(src_file, dest_file)

            st_src = os.stat(src_file)
            st_dest = os.stat(dest_file)

            self.assertEqual(st_src.st_atime, st_dest.st_atime)
            self.assertEqual(st_src.st_mtime, st_dest.st_mtime)


class TestFunctionCopyFileIfDifferent(unittest.TestCase):
    """
    Tests the copy_file_if_different() function.

    """

    def test_simple_copy(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_file_if_different(src_file, dest_file)

            data = None
            with open(dest_file, "r") as f:
                data = f.read()

            self.assertEqual(3, len(data))
            self.assertEqual("foo", data)

    def test_missing_src_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file_if_different,
                              src_file, dest_file)

    def test_src_symlink_dest_missing(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            os.symlink(src_file, src_file)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file_if_different,
                              src_file, dest_file)

    def test_src_file_dest_symlink(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            os.symlink(dest_file, dest_file)

            uriel.copy_file_if_different(src_file, dest_file)

            data = None
            with open(dest_file, "r") as f:
                data = f.read()

            self.assertFalse(os.path.islink(dest_file))
            self.assertEqual(3, len(data))
            self.assertEqual("foo", data)

    def test_src_symlink_dest_symlink(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            symlink_target = os.path.join(tmp_dir, "symlink_target")
            src_symlink = os.path.join(tmp_dir, "src_symlink")
            dest_symlink = os.path.join(tmp_dir, "dest_symlink")

            with open(symlink_target, "w") as f:
                f.write("foo")
                f.close()

            os.symlink(symlink_target, src_symlink)
            os.symlink(dest_symlink, dest_symlink)

            uriel.copy_file_if_different(src_symlink, dest_symlink)

            self.assertTrue(os.path.islink(dest_symlink))
            self.assertEqual(symlink_target, os.readlink(dest_symlink))

    def test_src_file_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            os.mkdir(dest_dir)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file_if_different,
                              src_file, dest_dir)

    def test_src_dir_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file_if_different,
                              src_dir, dest_dir)

    def test_src_dir_dest_missing(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_file = os.path.join(tmp_dir, "dest_file")

            os.mkdir(src_dir)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file_if_different,
                              src_dir, dest_file)

    def test_src_permission_error(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            os.chmod(src_file, 0)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file_if_different,
                              src_file, dest_file)

    def test_dest_permission_error(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            with open(dest_file, "w") as f:
                f.close()

            os.chmod(dest_file, 0)

            self.assertRaises(uriel.UrielError,
                              uriel.copy_file_if_different,
                              src_file, dest_file)

    def test_skip_copy_acceptable_false_positive(self):
        # this test demonstrates technically incorrect behavior,
        # but the situation is so contrived that you would have to
        # be trying to trick the system to realistically run into it
        #
        # basically, everything about the two files is the same, except
        # that the contents don't match. but the whole point of skipping
        # file copies is for major efficiency gains, and this situation
        # is extremely contrived, so the trade-off is worth it
        #
        # in pure logic terms, this could be considered a bug
        # in performance terms, it's a feature

        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            # write 8 bytes to src_file
            with open(src_file, "w") as f:
                f.write("SRC FILE ")
                f.close()

            # write 8 *different* bytes to dest_file
            with open(dest_file, "w") as f:
                f.write("DEST FILE")
                f.close()

            # make all of the file metadata match from src to dest
            #
            # the files already have the same number of bytes,
            # are both actual files (and not mismatched symlinks),
            # and should already have the same file permissions
            #
            # all that's left is to make the mtime values match
            st = os.stat(src_file)
            os.utime(dest_file, times=(st.st_atime, st.st_mtime))

            # copy the file if different, which will skip the copy in this
            # case, since of the metadata matches perfectly
            uriel.copy_file_if_different(src_file, dest_file)

            with open(src_file, "r") as f:
                self.assertEqual("SRC FILE ", f.read())

            with open(dest_file, "r") as f:
                self.assertEqual("DEST FILE", f.read())


class TestFunctionCopyFilesRecursive(unittest.TestCase):
    """
    Tests the copy_files_recursive() function.

    """

    # copy_files_recursive() ultimately calls copy_file_if_different()
    # whenever it copies a file/symlink/etc. therefore, the focus of
    # testing here is on basic recursive directory operations, trusting
    # that the individual file copy operations are already covered by
    # the copy_file_if_different() and copy_file() tests

    def test_file_copy(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            # normally this function is called with directories as
            # arguments, but it can do file copies, just for completeness
            uriel.copy_files_recursive(src_file, dest_file)

            data = None
            with open(dest_file, "r") as f:
                data = f.read()

            self.assertEqual(3, len(data))
            self.assertEqual("foo", data)

    def test_empty_src_dir_no_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            os.mkdir(src_dir)

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))

    def test_empty_src_dir_empty_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))

    def test_src_dir_with_file_no_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")

            os.mkdir(src_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_with_file_empty_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_with_file_dest_dir_with_conflicting_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            with open(dest_file, "w") as f:
                f.write("bar")
                f.close()

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_with_file_dest_dir_with_other_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")
            other_file = os.path.join(dest_dir, "b")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            with open(other_file, "w") as f:
                f.write("bar")
                f.close()

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

            with open(other_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("bar", data)

    def test_src_dir_recursive_no_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            # a/b/c/d
            src_a_dir = os.path.join(src_dir, "a")
            src_b_dir = os.path.join(src_a_dir, "b")
            src_c_dir = os.path.join(src_b_dir, "c")
            src_d_file = os.path.join(src_c_dir, "d")
            dest_a_dir = os.path.join(dest_dir, "a")
            dest_b_dir = os.path.join(dest_a_dir, "b")
            dest_c_dir = os.path.join(dest_b_dir, "c")
            dest_d_file = os.path.join(dest_c_dir, "d")

            os.mkdir(src_dir)
            os.mkdir(src_a_dir)
            os.mkdir(src_b_dir)
            os.mkdir(src_c_dir)

            with open(src_d_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isdir(dest_a_dir))
            self.assertTrue(os.path.isdir(dest_b_dir))
            self.assertTrue(os.path.isdir(dest_c_dir))
            self.assertTrue(os.path.isfile(dest_d_file))

            with open(dest_d_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_recursive_empty_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            # a/b/c/d
            src_a_dir = os.path.join(src_dir, "a")
            src_b_dir = os.path.join(src_a_dir, "b")
            src_c_dir = os.path.join(src_b_dir, "c")
            src_d_file = os.path.join(src_c_dir, "d")
            dest_a_dir = os.path.join(dest_dir, "a")
            dest_b_dir = os.path.join(dest_a_dir, "b")
            dest_c_dir = os.path.join(dest_b_dir, "c")
            dest_d_file = os.path.join(dest_c_dir, "d")

            os.mkdir(src_dir)
            os.mkdir(src_a_dir)
            os.mkdir(src_b_dir)
            os.mkdir(src_c_dir)

            os.mkdir(dest_dir)

            with open(src_d_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isdir(dest_a_dir))
            self.assertTrue(os.path.isdir(dest_b_dir))
            self.assertTrue(os.path.isdir(dest_c_dir))
            self.assertTrue(os.path.isfile(dest_d_file))

            with open(dest_d_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_recursive_complex_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            # a/b/c/d
            src_a_dir = os.path.join(src_dir, "a")
            src_b_dir = os.path.join(src_a_dir, "b")
            src_c_dir = os.path.join(src_b_dir, "c")
            src_d_file = os.path.join(src_c_dir, "d")
            dest_a_dir = os.path.join(dest_dir, "a")
            dest_b_dir = os.path.join(dest_a_dir, "b")
            dest_c_dir = os.path.join(dest_b_dir, "c")
            dest_d_file = os.path.join(dest_c_dir, "d")

            extra_dest_file = os.path.join(dest_b_dir, "extra_file")

            os.mkdir(src_dir)
            os.mkdir(src_a_dir)
            os.mkdir(src_b_dir)
            os.mkdir(src_c_dir)

            os.mkdir(dest_dir)
            os.mkdir(dest_a_dir)
            os.mkdir(dest_b_dir)
            os.symlink(dest_c_dir, dest_c_dir)

            with open(src_d_file, "w") as f:
                f.write("foo")
                f.close()

            with open(extra_dest_file, "w") as f:
                f.write("extra")
                f.close()

            uriel.copy_files_recursive(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isdir(dest_a_dir))
            self.assertTrue(os.path.isdir(dest_b_dir))
            self.assertTrue(os.path.isdir(dest_c_dir))
            self.assertTrue(os.path.isfile(dest_d_file))
            self.assertTrue(os.path.isfile(extra_dest_file))

            with open(src_d_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

            with open(extra_dest_file, "r") as f:
                data = f.read()
                self.assertEqual(5, len(data))
                self.assertEqual("extra", data)


class TestFunctionCopyFilesRecursiveOverwrite(unittest.TestCase):
    """
    Tests the copy_files_recursive_overwrite() function.

    """

    # copy_files_recursive_overwrite() ultimately calls
    # copy_file_if_different() whenever it copies a file/symlink/etc.
    # therefore, the focus of testing here is on basic recursive directory
    # operations, trusting that the individual file copy operations are
    # already covered by the copy_file_if_different() and copy_file() tests

    def test_file_copy(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_file = os.path.join(tmp_dir, "src_file")
            dest_file = os.path.join(tmp_dir, "dest_file")

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            # normally this function is called with directories as
            # arguments, but it can do file copies, just for completeness
            uriel.copy_files_recursive_overwrite(src_file, dest_file)

            data = None
            with open(dest_file, "r") as f:
                data = f.read()

            self.assertEqual(3, len(data))
            self.assertEqual("foo", data)

    def test_empty_src_dir_no_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            os.mkdir(src_dir)

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))

    def test_empty_src_dir_empty_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))

    def test_src_dir_with_file_no_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")

            os.mkdir(src_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_with_file_empty_dest_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_with_file_dest_dir_with_conflicting_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            with open(dest_file, "w") as f:
                f.write("bar")
                f.close()

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_with_file_dest_dir_with_other_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            src_file = os.path.join(src_dir, "a")
            dest_file = os.path.join(dest_dir, "a")
            other_file = os.path.join(dest_dir, "b")

            os.mkdir(src_dir)
            os.mkdir(dest_dir)

            with open(src_file, "w") as f:
                f.write("foo")
                f.close()

            with open(other_file, "w") as f:
                f.write("bar")
                f.close()

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isfile(dest_file))

            with open(dest_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

            self.assertFalse(os.path.exists(other_file))

    def test_src_dir_recursive_no_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            # a/b/c/d
            src_a_dir = os.path.join(src_dir, "a")
            src_b_dir = os.path.join(src_a_dir, "b")
            src_c_dir = os.path.join(src_b_dir, "c")
            src_d_file = os.path.join(src_c_dir, "d")
            dest_a_dir = os.path.join(dest_dir, "a")
            dest_b_dir = os.path.join(dest_a_dir, "b")
            dest_c_dir = os.path.join(dest_b_dir, "c")
            dest_d_file = os.path.join(dest_c_dir, "d")

            os.mkdir(src_dir)
            os.mkdir(src_a_dir)
            os.mkdir(src_b_dir)
            os.mkdir(src_c_dir)

            with open(src_d_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isdir(dest_a_dir))
            self.assertTrue(os.path.isdir(dest_b_dir))
            self.assertTrue(os.path.isdir(dest_c_dir))
            self.assertTrue(os.path.isfile(dest_d_file))

            with open(dest_d_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_recursive_empty_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            # a/b/c/d
            src_a_dir = os.path.join(src_dir, "a")
            src_b_dir = os.path.join(src_a_dir, "b")
            src_c_dir = os.path.join(src_b_dir, "c")
            src_d_file = os.path.join(src_c_dir, "d")
            dest_a_dir = os.path.join(dest_dir, "a")
            dest_b_dir = os.path.join(dest_a_dir, "b")
            dest_c_dir = os.path.join(dest_b_dir, "c")
            dest_d_file = os.path.join(dest_c_dir, "d")

            os.mkdir(src_dir)
            os.mkdir(src_a_dir)
            os.mkdir(src_b_dir)
            os.mkdir(src_c_dir)

            os.mkdir(dest_dir)

            with open(src_d_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isdir(dest_a_dir))
            self.assertTrue(os.path.isdir(dest_b_dir))
            self.assertTrue(os.path.isdir(dest_c_dir))
            self.assertTrue(os.path.isfile(dest_d_file))

            with open(dest_d_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)

    def test_src_dir_recursive_complex_dest(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            src_dir = os.path.join(tmp_dir, "src_dir")
            dest_dir = os.path.join(tmp_dir, "dest_dir")

            # a/b/c/d
            src_a_dir = os.path.join(src_dir, "a")
            src_b_dir = os.path.join(src_a_dir, "b")
            src_c_dir = os.path.join(src_b_dir, "c")
            src_d_file = os.path.join(src_c_dir, "d")
            dest_a_dir = os.path.join(dest_dir, "a")
            dest_b_dir = os.path.join(dest_a_dir, "b")
            dest_c_dir = os.path.join(dest_b_dir, "c")
            dest_d_file = os.path.join(dest_c_dir, "d")

            extra_dest_file = os.path.join(dest_b_dir, "extra_file")

            os.mkdir(src_dir)
            os.mkdir(src_a_dir)
            os.mkdir(src_b_dir)
            os.mkdir(src_c_dir)

            os.mkdir(dest_dir)
            os.mkdir(dest_a_dir)
            os.mkdir(dest_b_dir)
            os.symlink(dest_c_dir, dest_c_dir)

            with open(src_d_file, "w") as f:
                f.write("foo")
                f.close()

            with open(extra_dest_file, "w") as f:
                f.write("extra")
                f.close()

            uriel.copy_files_recursive_overwrite(src_dir, dest_dir)

            self.assertTrue(os.path.isdir(dest_dir))
            self.assertTrue(os.path.isdir(dest_a_dir))
            self.assertTrue(os.path.isdir(dest_b_dir))
            self.assertTrue(os.path.isdir(dest_c_dir))
            self.assertTrue(os.path.isfile(dest_d_file))

            self.assertFalse(os.path.exists(extra_dest_file))
            self.assertFalse(os.path.isfile(extra_dest_file))

            with open(src_d_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)


class TestFunctionDeleteDirectoryRecursive(unittest.TestCase):
    """
    Tests the delete_directory_recursive() function.

    """

    def test_none(self):
        c = UrielContainer()
        uriel = c.uriel

        self.assertRaises(uriel.UrielError,
                          uriel.delete_directory_recursive,
                          None)

    def test_non_existent_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            non_existent_dir = os.path.join(tmp_dir, "does-not-exist")

            self.assertRaises(uriel.UrielError,
                              uriel.delete_directory_recursive,
                              non_existent_dir)

    def test_empty_dir(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            empty_dir = os.path.join(tmp_dir, "empty")

            os.mkdir(empty_dir)

            uriel.delete_directory_recursive(empty_dir)

            self.assertFalse(os.path.exists(empty_dir))

    def test_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            file_path = os.path.join(tmp_dir, "file")

            with open(file_path, "w") as f:
                f.write("foo")
                f.close()

            self.assertRaises(uriel.UrielError,
                              uriel.delete_directory_recursive,
                              file_path)

    def test_recursive_delete(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            a_dir = os.path.join(tmp_dir, "a")
            b_dir = os.path.join(a_dir, "b")
            c_dir = os.path.join(b_dir, "c")
            d_file = os.path.join(c_dir, "d")
            s_symlink = os.path.join(b_dir, "s")

            os.mkdir(a_dir)
            os.mkdir(b_dir)
            os.mkdir(c_dir)
            os.symlink(s_symlink, s_symlink)

            with open(d_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.delete_directory_recursive(a_dir)

            self.assertFalse(os.path.exists(a_dir))
            self.assertFalse(os.path.exists(b_dir))
            self.assertFalse(os.path.exists(c_dir))
            self.assertFalse(os.path.exists(d_file))
            self.assertFalse(os.path.exists(s_symlink))


class TestFunctionEscape(unittest.TestCase):
    """
    Tests the foo() function.

    """

    def test_none(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = None
        escaped = uriel.escape(unescaped)
        self.assertEqual("", escaped)

    def test_empty_string(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = ""
        escaped = uriel.escape(unescaped)
        self.assertEqual("", escaped)

    def test_a(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "a"
        escaped = uriel.escape(unescaped)
        self.assertEqual("a", escaped)

    def test_42(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "42"
        escaped = uriel.escape(unescaped)
        self.assertEqual("42", escaped)

    def test_multi_character_string(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "foo bar"
        escaped = uriel.escape(unescaped)
        self.assertEqual("foo bar", escaped)

    def test_ampersand(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "&"
        escaped = uriel.escape(unescaped)
        self.assertEqual("&amp;", escaped)

    def test_double_quote(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = '"'
        escaped = uriel.escape(unescaped)
        self.assertEqual("&quot;", escaped)

    def test_single_quote(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "'"
        escaped = uriel.escape(unescaped)
        self.assertEqual("&apos;", escaped)

    def test_greater_than(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = ">"
        escaped = uriel.escape(unescaped)
        self.assertEqual("&gt;", escaped)

    def test_less_than(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "<"
        escaped = uriel.escape(unescaped)
        self.assertEqual("&lt;", escaped)

    def test_html_tags(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "<b>Foo</b>"
        escaped = uriel.escape(unescaped)
        self.assertEqual("&lt;b&gt;Foo&lt;/b&gt;", escaped)

    def test_everything(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "<b><i>\"A\" & 'B'</i></b>"
        escaped = uriel.escape(unescaped)
        self.assertEqual(
            "&lt;b&gt;&lt;i&gt;&quot;A&quot; &amp; &apos;B&apos;&lt;/i&gt;&lt;/b&gt;",
            escaped)


class TestFunctionEscapeXml(unittest.TestCase):
    """
    Tests the escape_xml() function.

    """

    def test_none(self):
        c = UrielContainer()
        uriel = c.uriel

        self.assertRaises(Exception, uriel.escape_xml, None)

    def test_basic(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "<b>foo</b>"
        escaped = uriel.escape_xml(unescaped)
        self.assertEqual("<b>foo</b>", escaped)

    def test_cdata_open(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "<![CDATA["
        escaped = uriel.escape_xml(unescaped)
        self.assertEqual("&lt;![CDATA[", escaped)

    def test_cdata_close(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "]]>"
        escaped = uriel.escape_xml(unescaped)
        self.assertEqual("]]&gt;", escaped)

    def test_cdata_complex(self):
        c = UrielContainer()
        uriel = c.uriel

        unescaped = "<pre>multi\nline\n<![CDATA[ example\n ]]></pre>"
        escaped = uriel.escape_xml(unescaped)
        self.assertEqual(
            "<pre>multi\nline\n&lt;![CDATA[ example\n ]]&gt;</pre>",
            escaped)


class TestFunctionCreateFileNodeTree(unittest.TestCase):
    """
    Tests the create_file_node_tree() function.

    """

    def test_create_file_node_tree(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_dir = os.path.join(project_root, "nodes")
            foo_dir = os.path.join(nodes_dir, "foo")
            bar_dir = os.path.join(foo_dir, "bar")
            baz_dir = os.path.join(bar_dir, "baz")

            root_index_file = os.path.join(nodes_dir, "index")
            foo_index_file = os.path.join(foo_dir, "index")
            bar_index_file = os.path.join(bar_dir, "index")
            baz_index_file = os.path.join(baz_dir, "index")
            quux_file = os.path.join(baz_dir, "quux")

            os.mkdir(nodes_dir)
            os.mkdir(foo_dir)
            os.mkdir(bar_dir)
            os.mkdir(baz_dir)

            with open(root_index_file, "w") as f:
                f.close()

            with open(foo_index_file, "w") as f:
                f.close()

            with open(bar_index_file, "w") as f:
                f.close()

            with open(baz_index_file, "w") as f:
                f.close()

            with open(quux_file, "w") as f:
                f.close()

            root = uriel.create_file_node_tree(project_root)
            foo = root.find_node_by_path("foo/index")
            bar = root.find_node_by_path("foo/bar/index")
            baz = root.find_node_by_path("foo/bar/baz/index")
            quux = root.find_node_by_path("foo/bar/baz/quux")

            self.assertEqual("index", root.get_path())
            self.assertEqual("foo/index", foo.get_path())
            self.assertEqual("foo/bar/index", bar.get_path())
            self.assertEqual("foo/bar/baz/index", baz.get_path())
            self.assertEqual("foo/bar/baz/quux", quux.get_path())


class TestFunctionCreateTagNodeTree(unittest.TestCase):
    """
    Tests the create_tag_node_tree() function.

    """

    def test_create_tag_node_tree_no_tag_node(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            uriel.create_tag_node_tree(project_root, root, False)

            self.assertEqual(0, len(root.get_children()))

    def test_create_tag_node_tree_no_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            tag = uriel.VirtualNode(project_root, "tag", root)

            root.add_child(foo)
            root.add_child(tag)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            root.set_header("tag-node", "tag")
            foo.set_header("tags", "a")
            bar.set_header("tags", "b")
            baz.set_header("tags", "c")
            quux.set_header("tags", "a, b, c, d")

            uriel.create_tag_node_tree(project_root, root, False)

            # tag
            self.assertEqual(
                "<p><a href=\"/tag/a/\">a</a></p>\n" + \
                "<p><a href=\"/tag/b/\">b</a></p>\n" + \
                "<p><a href=\"/tag/c/\">c</a></p>\n" + \
                "<p><a href=\"/tag/d/\">d</a></p>",
                tag.get_header("__tag-list-html"))

            # tag/a
            tag_a = root.find_node_by_path("tag/a")
            self.assertEqual("a", tag_a.get_header("title"))
            self.assertEqual("false", tag_a.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"/foo/\">Foo</a></p>\n" + \
                "<p><a href=\"/foo/bar/baz/quux/\">Quux</a></p>",
                tag_a.get_header("__tag-list-html"))

            # tag/b
            tag_b = root.find_node_by_path("tag/b")
            self.assertEqual("b", tag_b.get_header("title"))
            self.assertEqual("false", tag_b.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"/foo/bar/\">Bar</a></p>\n" + \
                "<p><a href=\"/foo/bar/baz/quux/\">Quux</a></p>",
                tag_b.get_header("__tag-list-html"))

            # tag/c
            tag_c = root.find_node_by_path("tag/c")
            self.assertEqual("c", tag_c.get_header("title"))
            self.assertEqual("false", tag_c.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"/foo/bar/baz/\">Baz</a></p>\n" + \
                "<p><a href=\"/foo/bar/baz/quux/\">Quux</a></p>",
                tag_c.get_header("__tag-list-html"))

            # tag/d
            tag_d = root.find_node_by_path("tag/d")
            self.assertEqual("d", tag_d.get_header("title"))
            self.assertEqual("false", tag_d.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"/foo/bar/baz/quux/\">Quux</a></p>",
                tag_d.get_header("__tag-list-html"))

    def test_create_tag_node_tree_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            tag = uriel.VirtualNode(project_root, "tag", root)

            root.add_child(foo)
            root.add_child(tag)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            root.set_header("tag-node", "tag")
            foo.set_header("tags", "a")
            bar.set_header("tags", "b")
            baz.set_header("tags", "c")
            quux.set_header("tags", "a, b, c, d")

            uriel.create_tag_node_tree(project_root, root, True)

            # tag
            self.assertEqual(
                "<p><a href=\"https://example.com/tag/a/\">a</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/b/\">b</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/c/\">c</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/d/\">d</a></p>",
                tag.get_header("__tag-list-html-canonical"))

            # tag/a
            tag_a = root.find_node_by_path("tag/a")
            self.assertEqual("a", tag_a.get_header("title"))
            self.assertEqual("false", tag_a.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"https://example.com/foo/\">Foo</a></p>\n" + \
                "<p><a href=\"https://example.com/foo/bar/baz/quux/\">Quux</a></p>",
                tag_a.get_header("__tag-list-html-canonical"))

            # tag/b
            tag_b = root.find_node_by_path("tag/b")
            self.assertEqual("b", tag_b.get_header("title"))
            self.assertEqual("false", tag_b.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/\">Bar</a></p>\n" + \
                "<p><a href=\"https://example.com/foo/bar/baz/quux/\">Quux</a></p>",
                tag_b.get_header("__tag-list-html-canonical"))

            # tag/c
            tag_c = root.find_node_by_path("tag/c")
            self.assertEqual("c", tag_c.get_header("title"))
            self.assertEqual("false", tag_c.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/baz/\">Baz</a></p>\n" + \
                "<p><a href=\"https://example.com/foo/bar/baz/quux/\">Quux</a></p>",
                tag_c.get_header("__tag-list-html-canonical"))

            # tag/d
            tag_d = root.find_node_by_path("tag/d")
            self.assertEqual("d", tag_d.get_header("title"))
            self.assertEqual("false", tag_d.get_header("flat-url"))
            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/baz/quux/\">Quux</a></p>",
                tag_d.get_header("__tag-list-html-canonical"))


class TestFunctionCreateTagLinks(unittest.TestCase):
    """
    Tests the create_tag_links() function.

    """

    def test_create_tag_links_no_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            root.set_header("tags", "a, b, c")

            tag = uriel.VirtualNode(project_root, "tag", root)
            root.add_child(tag)

            uriel.create_tag_node_tree(project_root, root, False)

            self.assertEqual(
                "<a href=\"/tag/a/\">a</a>, " + \
                "<a href=\"/tag/b/\">b</a>, " + \
                "<a href=\"/tag/c/\">c</a>",
                uriel.create_tag_links(root, False))

    def test_create_tag_links_with_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("tag-node", "tag")
            root.set_header("tags", "a, b, c")

            tag = uriel.VirtualNode(project_root, "tag", root)
            root.add_child(tag)

            uriel.create_tag_node_tree(project_root, root, True)

            self.assertEqual(
                "<a href=\"https://example.com/tag/a/\">a</a>, " + \
                "<a href=\"https://example.com/tag/b/\">b</a>, " + \
                "<a href=\"https://example.com/tag/c/\">c</a>",
                uriel.create_tag_links(root, True))


class TestFunctionCreateTagLinksRecursive(unittest.TestCase):
    """
    Tests the create_tag_links_recursive() function.

    """

    def test_create_tag_links_recursive_no_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            tag = uriel.VirtualNode(project_root, "tag", root)

            root.add_child(foo)
            root.add_child(tag)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            foo.set_header("tags", "a")
            bar.set_header("tags", "b")
            baz.set_header("tags", "c")
            quux.set_header("tags", "a, b, c, d")

            uriel.create_tag_node_tree(project_root, root, False)

            uriel.create_tag_links_recursive(root, False)

            self.assertEqual("", root.get_header("__tag-list-html"))

            self.assertEqual(
                "<a href=\"/tag/a/\">a</a>",
                foo.get_header("__tag-list-html"))

            self.assertEqual(
                "<a href=\"/tag/b/\">b</a>",
                bar.get_header("__tag-list-html"))

            self.assertEqual(
                "<a href=\"/tag/c/\">c</a>",
                baz.get_header("__tag-list-html"))

            self.assertEqual(
                "<a href=\"/tag/a/\">a</a>, " + \
                "<a href=\"/tag/b/\">b</a>, " + \
                "<a href=\"/tag/c/\">c</a>, " + \
                "<a href=\"/tag/d/\">d</a>",
                quux.get_header("__tag-list-html"))

    def test_create_tag_links_recursive_with_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            root.set_header("canonical-url", "https://example.com")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            tag = uriel.VirtualNode(project_root, "tag", root)

            root.add_child(foo)
            root.add_child(tag)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            foo.set_header("tags", "a")
            bar.set_header("tags", "b")
            baz.set_header("tags", "c")
            quux.set_header("tags", "a, b, c, d")

            uriel.create_tag_node_tree(project_root, root, True)

            uriel.create_tag_links_recursive(root, True)

            self.assertEqual("", root.get_header("__tag-list-html-canonical"))

            self.assertEqual(
                "<a href=\"https://example.com/tag/a/\">a</a>",
                foo.get_header("__tag-list-html-canonical"))

            self.assertEqual(
                "<a href=\"https://example.com/tag/b/\">b</a>",
                bar.get_header("__tag-list-html-canonical"))

            self.assertEqual(
                "<a href=\"https://example.com/tag/c/\">c</a>",
                baz.get_header("__tag-list-html-canonical"))

            self.assertEqual(
                "<a href=\"https://example.com/tag/a/\">a</a>, " + \
                "<a href=\"https://example.com/tag/b/\">b</a>, " + \
                "<a href=\"https://example.com/tag/c/\">c</a>, " + \
                "<a href=\"https://example.com/tag/d/\">d</a>",
                quux.get_header("__tag-list-html-canonical"))


class TestFunctionCreateChildNodeListHtml(unittest.TestCase):
    """
    Tests the create_child_node_list_html() function.

    """

    def test_create_child_node_list_no_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)

            root.add_child(foo)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            uriel.create_child_node_list_html(root, False)

            self.assertEqual(
                "<p><a href=\"/foo/\">Foo</a></p>",
                root.get_header("__node-list-html"))

            self.assertEqual(
                "<p><a href=\"/foo/bar/\">Bar</a></p>",
                foo.get_header("__node-list-html"))

            self.assertEqual(
                "<p><a href=\"/foo/bar/baz/\">Baz</a></p>",
                bar.get_header("__node-list-html"))

            self.assertEqual(
                "<p><a href=\"/foo/bar/baz/quux/\">Quux</a></p>",
                baz.get_header("__node-list-html"))

            self.assertEqual(
                "",
                quux.get_header("__node-list-html"))

    def test_create_child_node_list_with_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)

            root.add_child(foo)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            uriel.create_child_node_list_html(root, True)

            self.assertEqual(
                "<p><a href=\"https://example.com/foo/\">Foo</a></p>",
                root.get_header("__node-list-html-canonical"))

            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/\">Bar</a></p>",
                foo.get_header("__node-list-html-canonical"))

            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/baz/\">Baz</a></p>",
                bar.get_header("__node-list-html-canonical"))

            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/baz/quux/\">Quux</a></p>",
                baz.get_header("__node-list-html-canonical"))

            self.assertEqual(
                "",
                quux.get_header("__node-list-html-canonical"))


class TestFunctionAugmentNodeTree(unittest.TestCase):
    """
    Tests the augment_node_tree() function.

    """

    def test_augment_node_tree_no_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            tag = uriel.VirtualNode(project_root, "tag", root)

            root.add_child(foo)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)
            root.add_child(tag)

            foo.set_header("tags", "a")
            bar.set_header("tags", "b")
            baz.set_header("tags", "c")
            quux.set_header("tags", "a, b, c, d")

            uriel.augment_node_tree(project_root, root)

            # root
            self.assertEqual(
                "<p><a href=\"/tag/\">Tag</a></p>\n" + \
                "<p><a href=\"/foo/\">Foo</a></p>",
                root.get_header("__node-list-html"))
            self.assertEqual("", root.get_header("__tag-list-html"))

            # foo
            self.assertEqual(
                "<p><a href=\"/foo/bar/\">Bar</a></p>",
                foo.get_header("__node-list-html"))
            self.assertEqual(
                "<a href=\"/tag/a/\">a</a>",
                foo.get_header("__tag-list-html"))

            # bar
            self.assertEqual(
                "<p><a href=\"/foo/bar/baz/\">Baz</a></p>",
                bar.get_header("__node-list-html"))
            self.assertEqual(
                "<a href=\"/tag/b/\">b</a>",
                bar.get_header("__tag-list-html"))

            # baz
            self.assertEqual(
                "<p><a href=\"/foo/bar/baz/quux/\">Quux</a></p>",
                baz.get_header("__node-list-html"))
            self.assertEqual(
                "<a href=\"/tag/c/\">c</a>",
                baz.get_header("__tag-list-html"))

            # quux
            self.assertEqual(
                "",
                quux.get_header("__node-list-html"))
            self.assertEqual(
                "<a href=\"/tag/a/\">a</a>, " + \
                "<a href=\"/tag/b/\">b</a>, " + \
                "<a href=\"/tag/c/\">c</a>, " + \
                "<a href=\"/tag/d/\">d</a>",
                quux.get_header("__tag-list-html"))

            # tag
            self.assertIsNotNone(tag.created)
            self.assertIsNotNone(tag.modified)
            self.assertEqual(
                "<p><a href=\"/tag/a/\">a</a></p>\n" + \
                "<p><a href=\"/tag/b/\">b</a></p>\n" + \
                "<p><a href=\"/tag/c/\">c</a></p>\n" + \
                "<p><a href=\"/tag/d/\">d</a></p>",
                tag.get_header("__node-list-html"))
            self.assertEqual(
                "<p><a href=\"/tag/a/\">a</a></p>\n" + \
                "<p><a href=\"/tag/b/\">b</a></p>\n" + \
                "<p><a href=\"/tag/c/\">c</a></p>\n" + \
                "<p><a href=\"/tag/d/\">d</a></p>",
                tag.get_header("__tag-list-html"))

    def test_augment_node_tree_with_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("tag-node", "tag")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            tag = uriel.VirtualNode(project_root, "tag", root)

            root.add_child(foo)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)
            root.add_child(tag)

            foo.set_header("tags", "a")
            bar.set_header("tags", "b")
            baz.set_header("tags", "c")
            quux.set_header("tags", "a, b, c, d")

            uriel.augment_node_tree(project_root, root)

            # root
            self.assertEqual(
                "<p><a href=\"https://example.com/tag/\">Tag</a></p>\n" + \
                "<p><a href=\"https://example.com/foo/\">Foo</a></p>",
                root.get_header("__node-list-html-canonical"))
            self.assertEqual("", root.get_header("__tag-list-html-canonical"))

            # foo
            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/\">Bar</a></p>",
                foo.get_header("__node-list-html-canonical"))
            self.assertEqual(
                "<a href=\"https://example.com/tag/a/\">a</a>",
                foo.get_header("__tag-list-html-canonical"))

            # bar
            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/baz/\">Baz</a></p>",
                bar.get_header("__node-list-html-canonical"))
            self.assertEqual(
                "<a href=\"https://example.com/tag/b/\">b</a>",
                bar.get_header("__tag-list-html-canonical"))

            # baz
            self.assertEqual(
                "<p><a href=\"https://example.com/foo/bar/baz/quux/\">Quux</a></p>",
                baz.get_header("__node-list-html-canonical"))
            self.assertEqual(
                "<a href=\"https://example.com/tag/c/\">c</a>",
                baz.get_header("__tag-list-html-canonical"))

            # quux
            self.assertEqual(
                "",
                quux.get_header("__node-list-html-canonical"))
            self.assertEqual(
                "<a href=\"https://example.com/tag/a/\">a</a>, " + \
                "<a href=\"https://example.com/tag/b/\">b</a>, " + \
                "<a href=\"https://example.com/tag/c/\">c</a>, " + \
                "<a href=\"https://example.com/tag/d/\">d</a>",
                quux.get_header("__tag-list-html-canonical"))

            # tag
            self.assertIsNotNone(tag.created)
            self.assertIsNotNone(tag.modified)
            self.assertEqual(
                "<p><a href=\"https://example.com/tag/a/\">a</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/b/\">b</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/c/\">c</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/d/\">d</a></p>",
                tag.get_header("__node-list-html-canonical"))
            self.assertEqual(
                "<p><a href=\"https://example.com/tag/a/\">a</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/b/\">b</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/c/\">c</a></p>\n" + \
                "<p><a href=\"https://example.com/tag/d/\">d</a></p>",
                tag.get_header("__tag-list-html-canonical"))


class TestFunctionRenderNodeTree(unittest.TestCase):
    """
    Tests the render_node_tree() function.

    """

    def test_render_node_tree(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            templates_dir = os.path.join(project_root, "templates")
            template_file = os.path.join(templates_dir, "default.html")

            os.mkdir(templates_dir)

            with open(template_file, "w") as f:
                f.write("<p>\n")
                f.write("{{value:foo}}\n")
                f.write("</p>")
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")

            child = uriel.VirtualNode(project_root, "child", root)
            child.set_header("foo", "quux")

            root.add_child(child)

            uriel.render_node_tree(project_root, root)

            self.assertEqual("<p>\nbar\n</p>\n", root.get_rendered_body())
            self.assertEqual("<p>\nquux\n</p>\n", child.get_rendered_body())


class TestFunctionGetMaxUrlPathLen(unittest.TestCase):
    """
    Tests the get_max_url_path_len() function.

    """

    def test_get_max_url_path_len(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # /, index
            root = uriel.VirtualNode(project_root, "index")
            self.assertEqual((1,5), uriel.get_max_url_path_len(root))

            # /foo/, foo/index
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)
            self.assertEqual((5,9), uriel.get_max_url_path_len(foo))

            # /foo/bar/, foo/bar/index
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            foo.add_child(bar)
            self.assertEqual((9,13), uriel.get_max_url_path_len(bar))

            # /foo/bar/baz/, foo/bar/baz/index
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            bar.add_child(baz)
            self.assertEqual((13,17), uriel.get_max_url_path_len(baz))

            # /foo/bar/baz/quux/, foo/bar/baz/quux
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            baz.add_child(quux)
            self.assertEqual((18,16), uriel.get_max_url_path_len(quux))


class TestFunctionWriteDynamicNodes(unittest.TestCase):
    """
    Tests the write_dynamic_nodes() function.

    """

    def test_write_dynamic_nodes(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar", foo)

            root.add_child(foo)
            foo.add_child(bar)

            root.set_rendered_body("root")
            foo.set_rendered_body("foo")
            bar.set_rendered_body("bar")

            unique_urls = set()

            uriel.write_dynamic_nodes(project_root, root)

            root_index = os.path.join(public_dir, "index.html")
            foo_index = os.path.join(public_dir, "foo/index.html")
            bar_index = os.path.join(public_dir, "foo/bar/index.html")

            with open(root_index, "r") as f:
                content = f.read()
                self.assertEqual("root", content)

            with open(foo_index, "r") as f:
                content = f.read()
                self.assertEqual("foo", content)

            with open(bar_index, "r") as f:
                content = f.read()
                self.assertEqual("bar", content)

            self.assertEqual(8, len(c.stderr))
            self.assertEqual(
                "creating pages in '" + public_dir + "' from nodes and templates",
                c.stderr[0])
            self.assertEqual("--------+-----------+----------", c.stderr[1])
            self.assertEqual("type    | node      | url", c.stderr[2])
            self.assertEqual("--------+-----------+----------", c.stderr[3])
            self.assertEqual("virtual | index     | /", c.stderr[4])
            self.assertEqual("virtual | foo/index | /foo/", c.stderr[5])
            self.assertEqual("virtual | foo/bar   | /foo/bar/", c.stderr[6])
            self.assertEqual("--------+-----------+----------", c.stderr[7])


class TestFunctionWriteNodes(unittest.TestCase):
    """
    Tests the write_nodes() function.

    """

    def test_write_nodes(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar", foo)

            root.add_child(foo)
            foo.add_child(bar)

            root.set_rendered_body("root")
            foo.set_rendered_body("foo")
            bar.set_rendered_body("bar")

            unique_urls = set()

            # max_url_len = 9,  /foo/bar/
            # max_path_len = 9, foo/index
            uriel.write_nodes(project_root, root, 9, 9, unique_urls)

            root_index = os.path.join(public_dir, "index.html")
            foo_index = os.path.join(public_dir, "foo/index.html")
            bar_index = os.path.join(public_dir, "foo/bar/index.html")

            with open(root_index, "r") as f:
                content = f.read()
                self.assertEqual("root", content)

            with open(foo_index, "r") as f:
                content = f.read()
                self.assertEqual("foo", content)

            with open(bar_index, "r") as f:
                content = f.read()
                self.assertEqual("bar", content)

            self.assertEqual(3, len(c.stderr))
            self.assertEqual("virtual | index     | /", c.stderr[0])
            self.assertEqual("virtual | foo/index | /foo/", c.stderr[1])
            self.assertEqual("virtual | foo/bar   | /foo/bar/", c.stderr[2])


class TestFunctionGetEligibleNodes(unittest.TestCase):
    """
    Tests the get_eligible_nodes() function.

    """

    def test_get_eligible_nodes_default_false(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)

            root.add_child(foo)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            root.set_header("some-other-header", "true")
            foo.set_header("a", "true")
            baz.set_header("a", "false")
            quux.set_header("a", "true")

            eligible_nodes = set()

            uriel.get_eligible_nodes(root, "a", False, eligible_nodes)

            self.assertTrue(root not in eligible_nodes)
            self.assertTrue(foo in eligible_nodes)
            self.assertTrue(bar not in eligible_nodes)
            self.assertTrue(baz not in eligible_nodes)
            self.assertTrue(quux in eligible_nodes)

    def test_get_eligible_nodes_default_true(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)

            root.add_child(foo)
            foo.add_child(bar)
            bar.add_child(baz)
            baz.add_child(quux)

            root.set_header("some-other-header", "true")
            foo.set_header("a", "true")
            baz.set_header("a", "false")
            quux.set_header("a", "true")

            eligible_nodes = set()

            uriel.get_eligible_nodes(root, "a", True, eligible_nodes)

            self.assertTrue(root in eligible_nodes)
            self.assertTrue(foo in eligible_nodes)
            self.assertTrue(bar in eligible_nodes)
            self.assertTrue(baz not in eligible_nodes)
            self.assertTrue(quux in eligible_nodes)


class TestFunctionGetUtcOffset(unittest.TestCase):
    """
    Tests the get_utc_offset() function.

    """

    def test_get_utc_offset(self):
        os.environ["TZ"] = "America/Los_Angeles"
        is_dst = time.localtime().tm_isdst

        c = UrielContainer()
        uriel = c.uriel

        if is_dst:
            self.assertEqual(("-", "07", "00"), uriel.get_utc_offset())
        else:
            self.assertEqual(("-", "08", "00"), uriel.get_utc_offset())


class TestFunctionGetRfc2822Date(unittest.TestCase):
    """
    Tests the get_rfc_2822_date() function.

    """

    def test_get_rfc_2822_date(self):
        os.environ["TZ"] = "America/Los_Angeles"
        is_dst = time.localtime().tm_isdst

        c = UrielContainer()
        uriel = c.uriel

        dt = datetime.datetime.now()

        (sign, hh, mm) = uriel.get_utc_offset()
        expected = dt.strftime("%a, %d %b %Y %H:%M:%S ") + sign + hh + mm

        self.assertEqual(expected, uriel.get_rfc_2822_date(dt))


class TestFunctionGetW3cDatetime(unittest.TestCase):
    """
    Tests the get_w3c_datetime() function.

    """

    def test_get_w3c_datetime(self):
        os.environ["TZ"] = "America/Los_Angeles"
        is_dst = time.localtime().tm_isdst

        c = UrielContainer()
        uriel = c.uriel

        dt = datetime.datetime.now()

        (sign, hh, mm) = uriel.get_utc_offset()
        expected = dt.strftime("%Y-%m-%dT%H:%M:%S") + sign + hh + ":" + mm

        self.assertEqual(expected, uriel.get_w3c_datetime(dt))


class TestFunctionGetRssUrl(unittest.TestCase):
    """
    Tests the get_rss_url() function.

    """

    def test_get_rss_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertIsNone(uriel.get_rss_url(root))

    def test_get_rss_url_leading_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("rss-url", "/rss.xml")

            self.assertEqual("rss.xml", uriel.get_rss_url(root))

    def test_get_rss_url_no_leading_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("rss-url", "rss.xml")

            self.assertEqual("rss.xml", uriel.get_rss_url(root))

    def test_get_rss_url_directory_traversal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("rss-url", "../rss.xml")

            self.assertRaises(
                uriel.UrielError,
                uriel.get_rss_url,
                root)


class TestFunctionWriteRss(unittest.TestCase):
    """
    Tests the write_rss() function.

    """

    def test_write_rss_not_enabled(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            uriel.write_rss(project_root, root)

            self.assertEqual(0, len(c.stderr))

    def test_write_rss_no_items(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            rss_file = os.path.join(public_dir, "rss.xml")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("rss-url", "/rss.xml")
            root.set_header("rss-title", "My Website")
            root.set_header("rss-description", "All about my website")

            uriel.write_rss(project_root, root)

            self.assertTrue(os.path.isfile(rss_file))

            self.assertEqual(1, len(c.stderr))
            self.assertEqual("creating '" + rss_file + "'", c.stderr[0])

            with open(rss_file, "r") as f:
                contents = f.read()

                lines = contents.split("\n")

                self.assertEqual(10, len(lines))
                self.assertEqual(
                    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
                    lines[0])
                self.assertEqual(
                    "<rss version=\"2.0\">",
                    lines[1])
                self.assertEqual(
                    "<channel>",
                    lines[2])
                self.assertEqual(
                    "    <title>My Website</title>",
                    lines[3])
                self.assertEqual(
                    "    <link>https://example.com/</link>",
                    lines[4])
                self.assertEqual(
                    "    <description>All about my website</description>",
                    lines[5])
                self.assertTrue("<lastBuildDate>" in lines[6])
                self.assertTrue("</lastBuildDate>" in lines[6])
                self.assertEqual(
                    "</channel>",
                    lines[7])
                self.assertEqual(
                    "</rss>",
                    lines[8])
                self.assertEqual(
                    "",
                    lines[9])

    def test_write_rss(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            rss_file = os.path.join(public_dir, "rss.xml")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("rss-url", "/rss.xml")
            root.set_header("rss-title", "My Website")
            root.set_header("rss-description", "All about my website")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            foo.set_header("rss-include", "true")
            foo.set_body("foo")

            bar = uriel.VirtualNode(project_root, "foo/bar", foo)
            bar.set_header("rss-include", "true")
            bar.set_header("rss-add-node-title-header", "false")
            bar.set_body("bar")

            root.add_child(foo)
            root.add_child(bar)

            uriel.write_rss(project_root, root)

            self.assertTrue(os.path.isfile(rss_file))

            self.assertEqual(1, len(c.stderr))
            self.assertEqual("creating '" + rss_file + "'", c.stderr[0])

            with open(rss_file, "r") as f:
                contents = f.read()

                lines = contents.split("\n")

                self.assertEqual(24, len(lines))
                self.assertEqual(
                    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
                    lines[0])
                self.assertEqual(
                    "<rss version=\"2.0\">",
                    lines[1])
                self.assertEqual(
                    "<channel>",
                    lines[2])
                self.assertEqual(
                    "    <title>My Website</title>",
                    lines[3])
                self.assertEqual(
                    "    <link>https://example.com/</link>",
                    lines[4])
                self.assertEqual(
                    "    <description>All about my website</description>",
                    lines[5])
                self.assertTrue("<lastBuildDate>" in lines[6])
                self.assertTrue("</lastBuildDate>" in lines[6])
                self.assertEqual(
                    "    <item>",
                    lines[7])
                self.assertEqual(
                    "        <title>Bar</title>",
                    lines[8])
                self.assertEqual(
                    "        <link>https://example.com/foo/bar/</link>",
                    lines[9])
                self.assertEqual(
                    "        <description><![CDATA[bar]]></description>",
                    lines[10])
                self.assertTrue("<pubDate>" in lines[11])
                self.assertTrue("</pubDate>" in lines[11])
                self.assertEqual(
                    "    </item>",
                    lines[12])

                self.assertEqual(
                    "    <item>",
                    lines[13])
                self.assertEqual(
                    "        <title>Foo</title>",
                    lines[14])
                self.assertEqual(
                    "        <link>https://example.com/foo/</link>",
                    lines[15])
                self.assertEqual(
                    "        <description><![CDATA[<h1>Foo</h1>",
                    lines[16])
                self.assertEqual(
                    "",
                    lines[17])
                self.assertEqual(
                    "foo]]></description>",
                    lines[18])
                self.assertTrue("<pubDate>" in lines[19])
                self.assertTrue("</pubDate>" in lines[19])
                self.assertEqual(
                    "    </item>",
                    lines[20])
                self.assertEqual(
                    "</channel>",
                    lines[21])
                self.assertEqual(
                    "</rss>",
                    lines[22])
                self.assertEqual(
                    "",
                    lines[23])


class TestFunctionGetSitemapUrl(unittest.TestCase):
    """
    Tests the get_sitemap_url() function.

    """

    def test_get_sitemap_url_no_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertIsNone(uriel.get_sitemap_url(root))

    def test_get_sitemap_url_no_leading_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("sitemap-url", "sitemap.xml")

            self.assertEqual("sitemap.xml", uriel.get_sitemap_url(root))

    def test_get_sitemap_url_with_leading_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("sitemap-url", "/sitemap.xml")

            self.assertEqual("sitemap.xml", uriel.get_sitemap_url(root))

    def test_get_sitemap_url_directory_traversal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("sitemap-url", "../sitemap.xml")

            self.assertRaises(uriel.UrielError, uriel.get_sitemap_url, root)


class TestFunctionWriteSitemap(unittest.TestCase):
    """
    Tests the write_sitemap() function.

    """

    def test_write_sitemap_no_sitemap(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            uriel.write_sitemap(project_root, root)

            self.assertEqual(0, len(c.stderr))

    def test_write_sitemap_root_node(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            sitemap_file = os.path.join(public_dir, "sitemap.xml")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("sitemap-url", "/sitemap.xml")

            uriel.write_sitemap(project_root, root)

            self.assertEqual(1, len(c.stderr))
            self.assertEqual(
                "creating '" + sitemap_file + "'",
                c.stderr[0])

            with open(sitemap_file, "r") as f:
                contents = f.read()

                lines = contents.split("\n")

                self.assertEqual(8, len(lines))
                self.assertEqual(
                    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
                    lines[0])
                self.assertEqual(
                    "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
                    lines[1])
                self.assertEqual(
                    "    <url>",
                    lines[2])
                self.assertEqual(
                    "        <loc>https://example.com/</loc>",
                    lines[3])
                self.assertTrue("<lastmod>" in lines[4])
                self.assertTrue("</lastmod>" in lines[4])
                self.assertEqual(
                    "    </url>",
                    lines[5])
                self.assertEqual(
                    "</urlset>",
                    lines[6])
                self.assertEqual(
                    "",
                    lines[7])

    def test_write_sitemap(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            sitemap_file = os.path.join(public_dir, "sitemap.xml")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("sitemap-url", "/sitemap.xml")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)

            uriel.write_sitemap(project_root, root)

            self.assertEqual(1, len(c.stderr))
            self.assertEqual(
                "creating '" + sitemap_file + "'",
                c.stderr[0])

            with open(sitemap_file, "r") as f:
                contents = f.read()

                lines = contents.split("\n")

                self.assertEqual(12, len(lines))
                self.assertEqual(
                    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
                    lines[0])
                self.assertEqual(
                    "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
                    lines[1])
                self.assertEqual(
                    "    <url>",
                    lines[2])
                self.assertEqual(
                    "        <loc>https://example.com/foo/</loc>",
                    lines[3])
                self.assertTrue("<lastmod>" in lines[4])
                self.assertTrue("</lastmod>" in lines[4])
                self.assertEqual(
                    "    </url>",
                    lines[5])
                self.assertEqual(
                    "    <url>",
                    lines[6])
                self.assertEqual(
                    "        <loc>https://example.com/</loc>",
                    lines[7])
                self.assertTrue("<lastmod>" in lines[8])
                self.assertTrue("</lastmod>" in lines[8])
                self.assertEqual(
                    "    </url>",
                    lines[9])
                self.assertEqual(
                    "</urlset>",
                    lines[10])
                self.assertEqual(
                    "",
                    lines[11])


class TestFunctionWriteRobotsTxt(unittest.TestCase):
    """
    Tests the write_robots_txt() function.

    """

    def test_write_robots_txt_no_sitemap_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            robots_txt = os.path.join(project_root, "public/robots.txt")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")

            uriel.write_robots_txt(project_root, root)

            self.assertFalse(os.path.isfile(robots_txt))

    def test_write_robots_txt_with_sitemap_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            robots_txt = os.path.join(project_root, "public/robots.txt")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("sitemap-url", "sitemap.xml")

            uriel.write_robots_txt(project_root, root)

            self.assertTrue(os.path.isfile(robots_txt))

            with open(robots_txt, "r") as f:
                contents = f.read()

                self.assertEqual(
                    "Sitemap: https://example.com/sitemap.xml\n",
                    contents)


class TestFunctionGetDefaultTemplateContents(unittest.TestCase):
    """
    Tests the get_default_template_contents() function.

    """

    def test_get_default_template_contents(self):
        c = UrielContainer()
        uriel = c.uriel

        expected = \
            "<!DOCTYPE html>\n" + \
            "<html lang=\"en-US\">\n" + \
            "<head>\n" + \
            "    <title>{{node:title}}</title>\n" + \
            "</head>\n" + \
            "\n" + \
            "<body>\n" + \
            "\n" + \
            "<h1>{{node:title}}</h1>\n" + \
            "\n" + \
            "<p>The value of the <i>Foo</i> header is: \n" + \
            "<b>{{value:foo}}</b></p>\n" + \
            "\n" + \
            "{{node:body}}\n" + \
            "\n" + \
            "</body>\n" + \
            "</html>\n"

        self.assertEqual(
            expected,
            uriel.get_default_template_contents())


class TestFunctionGetDefaultIndexNodeContents(unittest.TestCase):
    """
    Tests the get_default_index_node_contents() function.

    """

    def test_get_default_index_node_contents(self):
        c = UrielContainer()
        uriel = c.uriel

        expected = \
            "Title: Hello World\n" + \
            "Foo: bar\n" + \
            "\n" + \
            "<p>This page is generated from a combination of the \n" + \
            "<i>index</i> node and the <i>default.html</i> \n" + \
            "template.</p>\n" + \
            "\n" + \
            "<p>Replace this with your own content, etc.</p>\n" + \
            "\n" + \
            "<p>This page was generated by uriel</p>\n"

        self.assertEqual(
            expected,
            uriel.get_default_index_node_contents())


class TestFunctionGetDefaultSojuContents(unittest.TestCase):
    """
    Tests the get_default_soju_contents() function.

    """

    def test_get_default_soju_contents(self):
        c = UrielContainer()
        uriel = c.uriel

        expected = \
            "##############################################################################\n" + \
            "# soju.py                                                                    #\n" + \
            "##############################################################################\n" + \
            "\n" + \
            "# The following symbols are imported using magic:\n" + \
            "#\n" + \
            "# import uriel\n" + \
            "# from uriel import SojuError\n" + \
            "# from uriel import log\n" + \
            "# from uriel import escape\n" + \
            "\n" + \
            "# The following variables are available to pass to functions:\n" + \
            "#\n" + \
            "# page\n" + \
            "# node\n" + \
            "# project_root\n" + \
            "# use_canonical_url\n" + \
            "\n" + \
            "# {{soju:node_title(node)}}\n" + \
            "def node_title(node):\n" + \
            "    return escape(node.get_title())\n" + \
            "\n"

        self.maxDiff = None
        self.assertEqual(
            expected,
            uriel.get_default_soju_contents())

class TestFunctionGetDefaultHandlersContents(unittest.TestCase):
    """
    Tests the get_default_handlers_contents() function.

    """

    def test_get_default_handlers_contents(self):
        c = UrielContainer()
        uriel = c.uriel

        expected = \
            "##############################################################################\n" + \
            "# handlers.py                                                                #\n" + \
            "##############################################################################\n" + \
            "\n" + \
            "# The following symbols are imported using magic:\n" + \
            "#\n" + \
            "# import uriel\n" + \
            "# from uriel import Page\n" + \
            "# from uriel import Node\n" + \
            "# from uriel import FileNode\n" + \
            "# from uriel import VirtualNode\n" + \
            "# from uriel import HandlerError\n" + \
            "# from uriel import log\n" + \
            "# from uriel import escape\n" + \
            "\n" + \
            "#def init(project_root):\n" + \
            "#    pass\n" + \
            "\n" + \
            "#def before_render_node_tree(project_root, root_node):\n" + \
            "#    pass\n" + \
            "\n" + \
            "#def after_render_node_tree(project_root, root_node):\n" + \
            "#    pass\n" + \
            "\n" + \
            "#def cleanup(project_root, root_node):\n" + \
            "#    pass\n" + \
            "\n"

        self.assertEqual(
            expected,
            uriel.get_default_handlers_contents())


class TestFunctionGetDefaultMakefileContents(unittest.TestCase):
    """
    Tests the get_default_makefile_contents() function.

    """

    def test_get_default_makefile_contents(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel_cmd = os.path.join(os.getcwd(), "uriel")

        expected = \
            "##############################################################################\n" + \
            "# uriel project Makefile                                                     #\n" + \
            "##############################################################################\n" + \
            "\n" + \
            "# path to uriel\n" + \
            "URIEL=" + uriel_cmd + "\n" + \
            "\n" + \
            "# uriel project subdirectories\n" + \
            "STATIC=static\n" + \
            "NODES=nodes\n" + \
            "TEMPLATES=templates\n" + \
            "PUBLIC=public\n" + \
            "LIB=lib\n" + \
            "\n" + \
            "##############################################################################\n" + \
            "# targets                                                                    #\n" + \
            "##############################################################################\n" + \
            "\n" + \
            ".PHONY: site clean preview\n" + \
            "\n" + \
            "site:\n" + \
            "\t${URIEL} .\n" + \
            "\n" + \
            "clean:\n" + \
            "\trm -rf ${PUBLIC}/\n" + \
            "\trm -rf ${LIB}/__pycache__\n" + \
            "\n" + \
            "preview: site\n" + \
            "\tcd ${PUBLIC}/ && python3 -m http.server\n" + \
            "\n"

        self.assertEqual(
            expected,
            uriel.get_default_makefile_contents())


class TestFunctionInitProjectRoot(unittest.TestCase):
    """
    Tests the init_project_root() function.

    """

    def test_init_project_root_new_project(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            uriel.init_project_root(project_root, True)

            self.assertEqual(10, len(c.stderr))
            self.assertEqual(
                "creating '" + project_root + "/nodes'",
                c.stderr[0])
            self.assertEqual(
                "creating '" + project_root + "/templates'",
                c.stderr[1])
            self.assertEqual(
                "creating '" + project_root + "/static'",
                c.stderr[2])
            self.assertEqual(
                "creating '" + project_root + "/lib'",
                c.stderr[3])
            self.assertEqual(
                "copying '" + project_root + "/static' to '" + \
                project_root + "/public', overwriting previous contents",
                c.stderr[4])
            self.assertEqual(
                "creating '" + project_root + "/templates/default.html'",
                c.stderr[5])
            self.assertEqual(
                "creating '" + project_root + "/nodes/index'",
                c.stderr[6])
            self.assertEqual(
                "creating '" + project_root + "/lib/soju.py'",
                c.stderr[7])
            self.assertEqual(
                "creating '" + project_root + "/lib/handlers.py'",
                c.stderr[8])
            self.assertEqual(
                "creating '" + project_root + "/Makefile'",
                c.stderr[9])

            self.assertTrue(os.path.isdir(os.path.join(project_root, "nodes")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "templates")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "static")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "lib")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "public")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "templates/default.html")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "nodes/index")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "lib/soju.py")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "lib/handlers.py")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "Makefile")))

    def test_init_project_root_existing_project_empty_directory(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            uriel.init_project_root(project_root, False)

            self.assertEqual(6, len(c.stderr))
            self.assertEqual(
                "creating '" + project_root + "/nodes'",
                c.stderr[0])
            self.assertEqual(
                "creating '" + project_root + "/templates'",
                c.stderr[1])
            self.assertEqual(
                "skipping static file copy, '" + \
                project_root + "/static' not found",
                c.stderr[2])
            self.assertEqual(
                "creating '" + project_root + "/public'",
                c.stderr[3])
            self.assertEqual(
                "creating '" + project_root + "/templates/default.html'",
                c.stderr[4])
            self.assertEqual(
                "creating '" + project_root + "/nodes/index'",
                c.stderr[5])

            self.assertTrue(os.path.isdir(os.path.join(project_root, "nodes")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "templates")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "static")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "lib")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "public")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "templates/default.html")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "nodes/index")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "lib/soju.py")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "lib/handlers.py")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "Makefile")))


class TestFunctionGetUrielModule(unittest.TestCase):
    """
    Tests the get_uriel_module() function.

    """

    def test_get_uriel_module(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel_module = None

        try:
            sys.modules["uriel"] = uriel
            uriel_module = uriel.get_uriel_module()
        finally:
            if "uriel" in sys.modules:
                del(sys.modules["uriel"])

        self.assertIsNotNone(uriel_module)
        self.assertEqual(uriel, uriel_module)


class TestFunctionInitModules(unittest.TestCase):
    """
    Tests the init_modules() function.

    """

    def test_init_modules_no_modules(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            soju_py = os.path.join(project_root, "lib/soju.py")
            handlers_py = os.path.join(project_root, "lib/handlers.py")

            os.mkdir(lib_dir)

            if "soju" in sys.modules:
                del(sys.modules["soju"])
            if "handlers" in sys.modules:
                del(sys.modules["handlers"])

            uriel.init_modules(project_root)

            self.assertEqual(2, len(c.stderr))

            self.assertEqual(
                "skipping module initialization, '" + soju_py + "' not found",
                c.stderr[0])

            self.assertEqual(
                "skipping module initialization, '" + handlers_py + "' not found",
                c.stderr[1])

    def test_init_modules_soju(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            soju_py = os.path.join(project_root, "lib/soju.py")
            handlers_py = os.path.join(project_root, "lib/handlers.py")

            os.mkdir(lib_dir)

            with open(soju_py, "w") as f:
                f.write("def foo():\n")
                f.write("    pass\n")
                f.close()

            if "soju" in sys.modules:
                del(sys.modules["soju"])
            if "handlers" in sys.modules:
                del(sys.modules["handlers"])

            try:
                sys.modules["uriel"] = uriel
                uriel.init_modules(project_root)
            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            self.assertEqual(2, len(c.stderr))
            self.assertEqual("initializing soju", c.stderr[0])
            self.assertEqual(
                "skipping module initialization, '" + handlers_py + "' not found",
                c.stderr[1])

    def test_init_modules_handlers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            soju_py = os.path.join(project_root, "lib/soju.py")
            handlers_py = os.path.join(project_root, "lib/handlers.py")

            os.mkdir(lib_dir)

            with open(handlers_py, "w") as f:
                f.write("def bar():\n")
                f.write("    pass\n")
                f.close()

            if "soju" in sys.modules:
                del(sys.modules["soju"])
            if "handlers" in sys.modules:
                del(sys.modules["handlers"])

            try:
                sys.modules["uriel"] = uriel
                uriel.init_modules(project_root)
            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            self.assertEqual(2, len(c.stderr))
            self.assertEqual(
                "skipping module initialization, '" + soju_py + "' not found",
                c.stderr[0])
            self.assertEqual("initializing handlers", c.stderr[1])

    def test_init_modules_both_modules(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            soju_py = os.path.join(project_root, "lib/soju.py")
            handlers_py = os.path.join(project_root, "lib/handlers.py")

            os.mkdir(lib_dir)

            with open(soju_py, "w") as f:
                f.write("def foo():\n")
                f.write("    pass\n")
                f.close()

            with open(handlers_py, "w") as f:
                f.write("def bar():\n")
                f.write("    pass\n")
                f.close()

            try:
                sys.modules["uriel"] = uriel
                uriel.init_modules(project_root)
            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            self.assertEqual(2, len(c.stderr))
            self.assertEqual("initializing soju", c.stderr[0])
            self.assertEqual("initializing handlers", c.stderr[1])


class TestFunctionWriteAdditionalFiles(unittest.TestCase):
    """
    Tests the write_additional_files() function.

    """

    def test_write_additional_files_no_resources(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            uriel.write_additional_files(project_root, root)

            self.assertEqual(0, len(c.stderr))

    def test_write_additional_files_minimal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")

            uriel.write_additional_files(project_root, root)

            self.assertEqual(0, len(c.stderr))

    def test_write_additional_files_sitemap_plus_robots(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("sitemap-url", "/sitemap.xml")

            uriel.write_additional_files(project_root, root)

            self.assertEqual(2, len(c.stderr))
            self.assertEqual(
                "creating '" + public_dir + "/sitemap.xml'",
                c.stderr[0])
            self.assertEqual(
                "creating '" + public_dir + "/robots.txt'",
                c.stderr[1])

    def test_write_additional_files_all(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")

            os.mkdir(public_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("sitemap-url", "/sitemap.xml")
            root.set_header("rss-url", "/rss.xml")
            root.set_header("rss-title", "My Website")
            root.set_header("rss-description", "All about my website")

            uriel.write_additional_files(project_root, root)

            self.assertEqual(3, len(c.stderr))
            self.assertEqual(
                "creating '" + public_dir + "/rss.xml'",
                c.stderr[0])
            self.assertEqual(
                "creating '" + public_dir + "/sitemap.xml'",
                c.stderr[1])
            self.assertEqual(
                "creating '" + public_dir + "/robots.txt'",
                c.stderr[2])


class TestFunctionCopyStaticFiles(unittest.TestCase):
    """
    Tests the copy_static_files() function.

    """

    def test_copy_static_files(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            static_dir = os.path.join(project_root, "static")
            public_dir = os.path.join(project_root, "public")

            # a/b/c/d
            static_a_dir = os.path.join(static_dir, "a")
            static_b_dir = os.path.join(static_a_dir, "b")
            static_c_dir = os.path.join(static_b_dir, "c")
            static_d_file = os.path.join(static_c_dir, "d")
            public_a_dir = os.path.join(public_dir, "a")
            public_b_dir = os.path.join(public_a_dir, "b")
            public_c_dir = os.path.join(public_b_dir, "c")
            public_d_file = os.path.join(public_c_dir, "d")

            os.mkdir(static_dir)
            os.mkdir(static_a_dir)
            os.mkdir(static_b_dir)
            os.mkdir(static_c_dir)

            os.mkdir(public_dir)

            with open(static_d_file, "w") as f:
                f.write("foo")
                f.close()

            uriel.copy_static_files(project_root)

            self.assertEqual(1, len(c.stderr))
            self.assertEqual(
                "copying '" + project_root + "/static' to '" + \
                project_root + "/public'",
                c.stderr[0])

            self.assertTrue(os.path.isdir(public_dir))
            self.assertTrue(os.path.isdir(public_a_dir))
            self.assertTrue(os.path.isdir(public_b_dir))
            self.assertTrue(os.path.isdir(public_c_dir))
            self.assertTrue(os.path.isfile(public_d_file))

            with open(public_d_file, "r") as f:
                data = f.read()
                self.assertEqual(3, len(data))
                self.assertEqual("foo", data)


class TestFunctionCreateProjectRoot(unittest.TestCase):
    """
    Tests the create_project_root() function.

    """

    def test_create_project_root_exists(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            self.assertFalse(uriel.create_project_root(project_root))

        self.assertEqual(0, len(c.stderr))

    def test_create_project_root_does_not_exist(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            project_root = os.path.join(tmp_dir, "my-project")

            self.assertTrue(uriel.create_project_root(project_root))

        self.assertEqual(1, len(c.stderr))
        self.assertEqual("creating '" + project_root + "'", c.stderr[0])


class TestFunctionCallHandler(unittest.TestCase):
    """
    Tests the call_handler() function.

    """

    def __get_handlers_py(self):
        return \
            "import os\n" + \
            "\n" + \
            "def basic(project_root, filename, value):\n" + \
            "    file_to_write = os.path.join(project_root, filename)\n" + \
            "    with open(file_to_write, \"w\") as f:\n" + \
            "        f.write(str(value))\n" + \
            "        f.write(\"\\n\")\n" + \
            "        f.close()\n" + \
            "\n" + \
            "def raise_handler_error():\n" + \
            "    raise HandlerError(\"HHH\")\n" + \
            "\n" + \
            "def raise_exception():\n" + \
            "    raise Exception(\"EEE\")\n"

    def test_call_handler_no_handlers_py(self):
        c = UrielContainer()
        uriel = c.uriel

        uriel.call_handler("no_handlers_py", "/some/file/path")

        self.assertIsNone(c.exit_code)
        self.assertEqual(0, len(c.stderr))

    def test_call_handler_function_not_defined(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            handlers_py = os.path.join(lib_dir, "handlers.py")
            test_file_txt = os.path.join(project_root, "test.txt")

            os.mkdir(lib_dir)

            with open(handlers_py, "w") as f:
                f.close()

            if "soju" in sys.modules:
                del(sys.modules["soju"])
            if "handlers" in sys.modules:
                del(sys.modules["handlers"])

            try:
                sys.modules["uriel"] = uriel
                uriel.init_modules(project_root)
            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            uriel.call_handler("function_not_defined", "blah")

            self.assertEqual(2, len(c.stderr))
            self.assertTrue("soju.py" in c.stderr[0])
            self.assertEqual("initializing handlers", c.stderr[1])

            self.assertFalse(os.path.isfile(test_file_txt))

    def test_call_handler_basic(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            handlers_py = os.path.join(lib_dir, "handlers.py")
            test_file_txt = os.path.join(project_root, "test.txt")

            os.mkdir(lib_dir)

            with open(handlers_py, "w") as f:
                f.write(self.__get_handlers_py())

            if "soju" in sys.modules:
                del(sys.modules["soju"])
            if "handlers" in sys.modules:
                del(sys.modules["handlers"])

            try:
                sys.modules["uriel"] = uriel
                uriel.init_modules(project_root)
            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            uriel.call_handler("basic", project_root, "test.txt", "42")

            self.assertEqual(3, len(c.stderr))
            self.assertTrue("soju.py" in c.stderr[0])
            self.assertEqual("initializing handlers", c.stderr[1])
            self.assertEqual("running handler: basic", c.stderr[2])

            self.assertTrue(os.path.isfile(test_file_txt))

            contents = None
            with open(test_file_txt, "r") as f:
                contents = f.read()

                self.assertEqual("42\n", contents)

    def test_call_handler_function_raises_handler_error(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            handlers_py = os.path.join(lib_dir, "handlers.py")
            test_file_txt = os.path.join(project_root, "test.txt")

            os.mkdir(lib_dir)

            with open(handlers_py, "w") as f:
                f.write(self.__get_handlers_py())

            if "soju" in sys.modules:
                del(sys.modules["soju"])
            if "handlers" in sys.modules:
                del(sys.modules["handlers"])

            try:
                sys.modules["uriel"] = uriel
                uriel.init_modules(project_root)
            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            self.assertRaises(uriel.HandlerError, uriel.call_handler,
                              "raise_handler_error")

            self.assertEqual(3, len(c.stderr))
            self.assertTrue("soju.py" in c.stderr[0])
            self.assertEqual("initializing handlers", c.stderr[1])
            self.assertEqual("running handler: raise_handler_error",
                             c.stderr[2])

    def test_call_handler_function_raises_exception(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            lib_dir = os.path.join(project_root, "lib")
            handlers_py = os.path.join(lib_dir, "handlers.py")
            test_file_txt = os.path.join(project_root, "test.txt")

            os.mkdir(lib_dir)

            with open(handlers_py, "w") as f:
                f.write(self.__get_handlers_py())

            if "soju" in sys.modules:
                del(sys.modules["soju"])
            if "handlers" in sys.modules:
                del(sys.modules["handlers"])

            try:
                sys.modules["uriel"] = uriel
                uriel.init_modules(project_root)
            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            self.assertRaises(uriel.HandlerError, uriel.call_handler,
                              "raise_exception")

            self.assertEqual(6, len(c.stderr))
            self.assertTrue("soju.py" in c.stderr[0])
            self.assertEqual("initializing handlers", c.stderr[1])
            self.assertEqual("running handler: raise_exception", c.stderr[2])
            self.assertEqual("Traceback (most recent call last):", c.stderr[3])
            self.assertTrue("  File " in c.stderr[4])
            self.assertEqual("Exception: 'EEE'", c.stderr[5])


class TestFunctionHandleProject(unittest.TestCase):
    """
    Tests the handle_project() function.

    """

    def test_handle_project_new_project(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            project_root = os.path.join(tmp_dir, "my-project")

            try:
                sys.modules["uriel"] = uriel
                uriel.handle_project(project_root)

            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            self.assertEqual(0, c.exit_code)
            self.assertEqual(22, len(c.stderr))
            self.assertEqual(
                "creating '" + project_root + "'",
                c.stderr[0])
            self.assertEqual(
                "creating '" + project_root + "/nodes'",
                c.stderr[1])
            self.assertEqual(
                "creating '" + project_root + "/templates'",
                c.stderr[2])
            self.assertEqual(
                "creating '" + project_root + "/static'",
                c.stderr[3])
            self.assertEqual(
                "creating '" + project_root + "/lib'",
                c.stderr[4])
            self.assertEqual(
                "copying '" + project_root + "/static' to '" + \
                project_root + "/public', overwriting previous contents",
                c.stderr[5])
            self.assertEqual(
                "creating '" + project_root + "/templates/default.html'",
                c.stderr[6])
            self.assertEqual(
                "creating '" + project_root + "/nodes/index'",
                c.stderr[7])
            self.assertEqual(
                "creating '" + project_root + "/lib/soju.py'",
                c.stderr[8])
            self.assertEqual(
                "creating '" + project_root + "/lib/handlers.py'", c.stderr[9])
            self.assertEqual(
                "creating '" + project_root + "/Makefile'",
                c.stderr[10])
            self.assertEqual(
                "initializing soju",
                c.stderr[11])
            self.assertEqual(
                "initializing handlers",
                c.stderr[12])
            self.assertEqual(
                "reading node files",
                c.stderr[13])
            self.assertEqual(
                "rendering node content",
                c.stderr[14])
            self.assertEqual(
                "creating pages in '" + \
                project_root + "/public' from nodes and templates",
                c.stderr[15])
            self.assertEqual(
                "--------+-------+----",
                c.stderr[16])
            self.assertEqual(
                "type    | node  | url",
                c.stderr[17])
            self.assertEqual(
                "--------+-------+----",
                c.stderr[18])
            self.assertEqual(
                "file    | index | /",
                c.stderr[19])
            self.assertEqual(
                "--------+-------+----",
                c.stderr[20])
            self.assertEqual(
                "copying '" + \
                project_root + "/static' to '" + project_root + "/public'",
                c.stderr[21])

            self.assertTrue(os.path.isdir(project_root))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "nodes")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "templates")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "static")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "lib")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "public")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "templates/default.html")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "nodes/index")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "lib/soju.py")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "lib/handlers.py")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "Makefile")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "public/index.html")))

    def test_handle_project_minimal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as tmp_dir:
            project_root = os.path.join(tmp_dir, "my-project")

            os.mkdir(project_root)

            try:
                sys.modules["uriel"] = uriel
                uriel.handle_project(project_root)

            finally:
                if "uriel" in sys.modules:
                    del(sys.modules["uriel"])

            self.assertEqual(0, c.exit_code)
            self.assertEqual(15, len(c.stderr))
            self.assertEqual(
                "creating '" + project_root + "/nodes'",
                c.stderr[0])
            self.assertEqual(
                "creating '" + project_root + "/templates'",
                c.stderr[1])
            self.assertEqual(
                "skipping static file copy, '" + project_root + "/static' not found",
                c.stderr[2])
            self.assertEqual(
                "creating '" + project_root + "/public'",
                c.stderr[3])
            self.assertEqual(
                "creating '" + project_root + "/templates/default.html'",
                c.stderr[4])
            self.assertEqual(
                "creating '" + project_root + "/nodes/index'",
                c.stderr[5])
            self.assertEqual(
                "skipping module initialization, '" + \
                project_root + "/lib' not found",
                c.stderr[6])
            self.assertEqual(
                "reading node files",
                c.stderr[7])
            self.assertEqual(
                "rendering node content",
                c.stderr[8])
            self.assertEqual(
                "creating pages in '" + \
                project_root + "/public' from nodes and templates",
                c.stderr[9])
            self.assertEqual(
                "--------+-------+----",
                c.stderr[10])
            self.assertEqual(
                "type    | node  | url",
                c.stderr[11])
            self.assertEqual(
                "--------+-------+----",
                c.stderr[12])
            self.assertEqual(
                "file    | index | /",
                c.stderr[13])
            self.assertEqual(
                "--------+-------+----",
                c.stderr[14])

            self.assertTrue(os.path.isdir(project_root))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "nodes")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "templates")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "static")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "lib")))
            self.assertTrue(os.path.isdir(os.path.join(project_root, "public")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "templates/default.html")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "nodes/index")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "lib/soju.py")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "lib/handlers.py")))
            self.assertFalse(os.path.exists(os.path.join(project_root, "Makefile")))
            self.assertTrue(os.path.isfile(os.path.join(project_root, "public/index.html")))

