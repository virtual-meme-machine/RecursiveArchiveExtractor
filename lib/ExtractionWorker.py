import os
import threading
import zipfile

import rarfile

from lib import StringManager, SimpleLogger, Utils


class ExtractionWorker(threading.Thread):
    """Handles extracting archive_file_list"""
    thread_active = True

    def __init__(self, main_panel_object):
        """Initialize object variables"""
        threading.Thread.__init__(self)
        self.main_panel_object = main_panel_object
        self.archive_file_list = self.main_panel_object.archive_file_list
        self.extract_path = str(self.main_panel_object.extract_path_entry_textbox.GetValue())
        self.main_panel_object.extract_in_progress = True
        SimpleLogger.log.info_msg(f"ExtractionWorker thread created. Extract path = '{self.extract_path}'")

    def run(self):
        """Main process for archive extraction thread"""
        extract_count = 0
        extract_range = len(self.archive_file_list)
        self.main_panel_object.extract_all_button.SetLabel(StringManager.SM.button_label_cancel)
        SimpleLogger.log.info_msg(f"ExtractionWorker thread started, extracting {extract_range} archive file(s)")

        # Close thread if the extraction path is not a directory
        if not os.path.isdir(self.extract_path):
            SimpleLogger.log.error_msg(f"Extract path '{self.extract_path}' does not exist, aborting")
            self.close_thread(cancelled=True)
            return

        # Close thread if the extraction path is not writable
        if not Utils.dir_is_writable(self.extract_path):
            SimpleLogger.log.error_msg(f"Extract path '{self.extract_path}' is not writable, aborting")
            self.close_thread(cancelled=True)
            return

        # Extract archive files
        for archive_file in self.archive_file_list:
            if not self.thread_active:
                SimpleLogger.log.info_msg("ExtractionWorker thread cancelled, aborting")
                return

            SimpleLogger.log.info_msg(f"Extracting archive {extract_count + 1}/{extract_range}")
            if archive_file.archive_format == ".rar":
                self.__extract_rar_file(archive_file.file_path)
            if archive_file.archive_format == ".zip":
                self.__extract_zip_file(archive_file.file_path)

            if not self.thread_active:
                SimpleLogger.log.info_msg("ExtractionWorker thread cancelled, aborting")
                return

            # Update progress bar
            extract_count += 1
            self.main_panel_object.refresh_progress_bar(extract_count, extract_range)

        # Close thread
        self.close_thread()
        return

    def close_thread(self, cancelled=False):
        """Refreshes UI elements that might have changed and close the thread"""
        if cancelled:
            self.main_panel_object.refresh_progress_bar(0, 0)

        self.main_panel_object.extract_all_button.SetLabel(StringManager.SM.button_label_extract_all)
        self.thread_active = False
        self.main_panel_object.extract_in_progress = False
        self.main_panel_object.extract_thread = None
        SimpleLogger.log.info_msg("ExtractionWorker thread closing")
        return

    def __extract_rar_file(self, rar_file_path):
        """Extracts a given RAR file"""
        SimpleLogger.log.info_msg(f"Extracting RAR file '{rar_file_path}'...")
        with rarfile.RarFile(rar_file_path) as rar_file:
            rar_file.extractall(self.extract_path)

    def __extract_zip_file(self, zip_file_path):
        """Extracts a given ZIP file"""
        SimpleLogger.log.info_msg(f"Extracting ZIP file '{zip_file_path}'...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            zip_file.extractall(self.extract_path)
