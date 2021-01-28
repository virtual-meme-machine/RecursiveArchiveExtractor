import locale
import json
import os

from lib import SimpleLogger

SM = None


class StringManager(object):
    """Stores localized strings used throughout the program"""
    window_title_main = None
    window_title_browse_dialog = None

    button_label_browse = None
    button_label_extract_all = None
    button_label_scan = None

    section_label_root_path = None
    section_label_file_list = None
    section_label_progress_bar = None
    section_label_extract_path = None

    file_list_file_name = None
    file_list_file_path = None
    file_list_archive_format = None
    file_list_archive_size = None

    file_count_init_message = None
    file_count_scan_start_message = None
    file_count_string_singular = None
    file_count_string_plural = None

    def __init__(self, json_file):
        """Initialize object variables"""
        self.__dict__ = self.__load_strings_from_json(json_file)
        SimpleLogger.log.info_msg(f"StringManager initialized using JSON file '{json_file}'")

    @staticmethod
    def __load_strings_from_json(json_file):
        """Loads localized strings from a JSON file"""
        try:
            if os.path.isfile(json_file):
                if os.path.splitext(json_file)[1] == ".json":
                    with open(json_file, "r") as json_data:
                        return json.load(json_data)
                else:
                    raise ValueError(f"File '{json_file}' is not a JSON file")
            else:
                raise FileNotFoundError(f"File '{json_file}' does not exist or is not a file")
        except (ValueError, FileNotFoundError) as err:
            error_msg = "Unable to load JSON file: {}".format(err)
            SimpleLogger.log.fatal_msg(error_msg)


def initialize_string_manager(data_dir):
    """Creates a static instance of the StringManager"""
    locale_code = locale.getdefaultlocale()[0]
    strings_file = os.path.join(data_dir, f"strings-{locale_code}.json")

    global SM
    SM = StringManager(strings_file)
