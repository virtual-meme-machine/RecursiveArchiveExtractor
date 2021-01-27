import datetime
import os
import tempfile

from lib import Utils

log = None

__LOG_FILE_NAME = "recursive_archive_extractor.log"


class SimpleLogger(object):
    """Simple logging class"""
    log_to_console = True
    log_to_file = True
    log_file_path = None

    __first_message_logged = False

    def __init__(self, log_file_name):
        """Initialize logger variables"""
        # Set log dir to temp if writable, if not log to current dir
        log_dir = tempfile.gettempdir()
        if not Utils.dir_is_writable(log_dir):
            log_dir = os.path.abspath(os.getcwd())

        self.log_file_path = os.path.join(log_dir, log_file_name)

    def __write_to_log(self, log_level, message):
        """Writes the given message to the log file as well as the console"""
        date_stamp = self.__get_date_stamp()
        class_path = Utils.get_class_path()
        log_msg = f"[{date_stamp}] [{log_level}] {class_path}:    {message}"

        if not self.__first_message_logged:
            self.__first_message_logged = True
            with open(self.log_file_path, "a") as log_file:
                log_file.write("\n\n")
            self.info_msg(f"Log file initialized at: '{self.log_file_path}'")

        if self.log_to_file:
            with open(self.log_file_path, "a") as log_file:
                log_file.write(log_msg)
                log_file.write("\n")

        if self.log_to_console:
            print(log_msg)

    @staticmethod
    def __get_date_stamp():
        """Returns a date stamp string"""
        date = datetime.datetime.now()
        return date.strftime("%Y-%m-%d %H:%M:%S:%f")

    def info_msg(self, message):
        """Logs an INFO message"""
        self.__write_to_log("INFO", message)

    def error_msg(self, message):
        """Logs an ERROR message"""
        self.__write_to_log("ERROR", message)

    def fatal_msg(self, message, exit_code=1):
        """Logs an FATAL message"""
        self.__write_to_log("FATAL", message)
        exit(exit_code)


def initialize_logger():
    """Creates a static instance of the logger"""
    global log
    log = SimpleLogger(__LOG_FILE_NAME)
