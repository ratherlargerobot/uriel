import os
import shutil
import tempfile
import datetime
import importlib
import importlib.util

##############################################################################
# CLASSES                                                                    #
##############################################################################

class TempDir:
    """
    Context manager class to create and remove a temporary directory.

    Usage:

        with TempDir() as tmp_dir:
            # do stuff with the temporary directory...

    """

    def __enter__(self):
        """
        Create a temporary directory, and return the directory name.

        """

        self.__tmp_dir = tempfile.mkdtemp(prefix=".uriel-testsuite-")
        return self.__tmp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Recursively remove the temporary directory that was created
        by the __enter__() method.

        """

        if os.path.isdir(self.__tmp_dir):
            shutil.rmtree(self.__tmp_dir)

class UrielContainer:
    """
    Loads the uriel script as a module, nested inside of this class.

    Remaps the sys_exit() and log() functions in uriel, which exit
    the program, and print to stderr, respectively.

    The exit code and stderr messages can instead be retrieved from
    variables in this class.

    Usage:

        # create container
        c = UrielContainer()

        # get uriel module reference from container
        uriel = c.uriel

        # now you can reference classes and functions under uriel.*
        uriel.show_usage()

        # retrieve program exit code (or None)
        print(c.exit_code)

        # retrieve printed stderr messages as a list
        for line in c.stderr:
            print(line)

    """

    def __init__(self):
        # this is roughly equivalent to 'import uriel',
        # but then storing the module reference as self.uriel
        # (however, we intentionally don't add it to sys.modules)
        loader = importlib.machinery.SourceFileLoader("uriel", "./uriel")
        spec = importlib.util.spec_from_loader("uriel", loader)
        self.uriel = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.uriel)

        # remap uriel.sys_exit() and uriel.log() functions
        # so that we can capture the results here for tests,
        # instead of letting the original implementations call functions like
        # sys.exit() and sys.stderr.write()

        self.exit_code = None
        self.stderr = []

        def sys_exit(exit_code):
            self.exit_code = exit_code

        def log(s):
            self.stderr.append(s)

        self.uriel.sys_exit = sys_exit
        self.uriel.log = log

##############################################################################
# FUNCTIONS                                                                  #
##############################################################################

def get_datetime_from_date_str(date_str):
    """
    Get a datetime.datetime instance from the provided date string.

    The date string must be in the ISO 8601 date format.

    """

    try:
        # turn the date string into a datetime instance
        dt = datetime.datetime.fromisoformat(date_str)

        # if the datetime instance doesn't have a time zone,
        # create a new datetime with the date/time we read from
        # the date string, augmented with the local time zone
        if dt.tzinfo is None:
            tmp_dt = datetime.datetime.fromtimestamp(
                dt.timestamp(),
                datetime.datetime.now(datetime.UTC).astimezone().tzinfo)

            dt = tmp_dt

        # return the datetime with time zone
        return dt

    except Exception as e:
        err = "invalid date header value in node " + \
              "'%s': '%s'"
        raise Exception(err % (self.get_path(), date_str))

