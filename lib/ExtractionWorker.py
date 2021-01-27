import os
import threading
import zipfile

import rarfile


class ExtractionWorker(threading.Thread):
    """Handles extracting archive_file_list"""

    def __init__(self, main_panel_object):
        """Initialize object variables"""
        threading.Thread.__init__(self)
        self.main_panel_object = main_panel_object
        self.archive_file_list = self.main_panel_object.archive_file_list
        self.extract_path = str(self.main_panel_object.extract_path_entry_textbox.GetValue())

    def run(self):
        """Main process for archive extraction thread"""
        extract_count = 0
        extract_range = len(self.archive_file_list)

        # Close thread if the extraction path is not a directory
        if not os.path.isdir(self.extract_path):
            return

        # Extract archive files
        for archive_file in self.archive_file_list:
            if archive_file.archive_format == ".rar":
                self.__extract_rar_file(archive_file.file_path)
            if archive_file.archive_format == ".zip":
                self.__extract_zip_file(archive_file.file_path)

            # Update progress bar
            extract_count += 1
            self.main_panel_object.refresh_progress_bar(extract_count, extract_range)

        # Close thread
        self.main_panel_object.extract_in_progress = False
        return

    def __extract_rar_file(self, rar_file_path):
        """Extracts a given RAR file"""
        with rarfile.RarFile(rar_file_path) as rar_file:
            rar_file.extractall(self.extract_path)

    def __extract_zip_file(self, zip_file_path):
        """Extracts a given ZIP file"""
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            zip_file.extractall(self.extract_path)
