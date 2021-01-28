import os
import re
import threading

from lib import ArchiveObject, StringManager, SimpleLogger

SUPPORTED_ARCHIVE_FORMATS = [".rar", ".zip"]
PARTIAL_FILE_REGEX = [r"[\S\s]*(\.part([\d]*)\.)[\S\s]*"]


class ArchiveScanner(threading.Thread):
    """Scans a given root path recursively to generate a list of ArchiveObjects for located archive files"""
    thread_active = True

    def __init__(self, main_panel_object):
        """Initialize object variables"""
        threading.Thread.__init__(self)
        self.main_panel_object = main_panel_object
        self.root_path = self.main_panel_object.root_path_entry_textbox.GetValue()
        self.main_panel_object.scan_in_progress = True
        SimpleLogger.log.info_msg(f"ArchiveScanner thread created. Root path = '{self.root_path}'")

    def run(self):
        """Main process for archive scanning thread"""
        archive_file_list = self.main_panel_object.archive_file_list
        SimpleLogger.log.info_msg("ArchiveScanner thread started, initiating scan")

        # Clear archive_file_list, reset control list, set file counter to scanning message
        archive_file_list.clear()
        SimpleLogger.log.info_msg("Archive file list cleared")
        self.main_panel_object.refresh_file_list_contents()
        self.main_panel_object.file_count_text.SetLabel(StringManager.SM.file_count_scan_start_message)
        self.main_panel_object.root_path_entry_scan_button.SetLabel(StringManager.SM.button_label_cancel)

        if not os.path.isdir(self.root_path):
            SimpleLogger.log.error_msg(f"Root path '{self.root_path}' does not exist, aborting")
            self.close_thread(cancelled=True)
            return

        archive_folders = self.__find_archive_folders()
        if archive_folders is None:
            SimpleLogger.log.info_msg("No folders containing archive files were found, aborting")
            self.close_thread(cancelled=True)
            return

        if not self.thread_active:
            SimpleLogger.log.info_msg("ArchiveScanner thread cancelled, aborting")
            return

        # Compile list of file paths to be extracted
        SimpleLogger.log.info_msg("Creating ArchiveObjects for archive files and adding to archive file list")
        for folder in archive_folders:
            if not self.thread_active:
                SimpleLogger.log.info_msg("ArchiveScanner thread cancelled, aborting")
                return

            for file in archive_folders.get(folder):
                if not self.thread_active:
                    SimpleLogger.log.info_msg("ArchiveScanner thread cancelled, aborting")
                    return

                if os.path.isfile(os.path.join(folder, file)):
                    file_name = file
                    file_path = os.path.join(folder, file)
                    archive_format = self.__determine_archive_format(file_name)
                    archive_size = os.path.getsize(file_path)
                    archive_file_list.append(ArchiveObject.ArchiveObject(file_path, file_name, archive_format, archive_size))
                    self.main_panel_object.refresh_file_count()

        SimpleLogger.log.info_msg(f"Found: {len(archive_file_list)} archive files. Scan complete")

        if not self.thread_active:
            SimpleLogger.log.info_msg("ArchiveScanner thread cancelled, aborting")
            return

        # Update file list control to reflect changes and close thread
        self.close_thread()
        return

    def close_thread(self, cancelled=False):
        """Refreshes UI elements that might have changed and close the thread"""
        if cancelled:
            self.main_panel_object.archive_file_list.clear()

        self.main_panel_object.refresh_file_list_contents()
        self.main_panel_object.root_path_entry_scan_button.SetLabel(StringManager.SM.button_label_scan)
        self.main_panel_object.scan_in_progress = False
        self.thread_active = False
        self.main_panel_object.scan_thread = None
        SimpleLogger.log.info_msg("ArchiveScanner thread closing")
        return

    def __find_archive_folders(self):
        """Walk root path to find folders that contain archive files, return data as dictionary"""
        archive_folders = {}
        ############################################################################
        # Dictionary that stores file paths and lists of extractable files in them #
        # archive_folders:                                                         #
        # {                                                                        #
        #     "/path/to/folder1": ["file1.rar", "file2.rar", "file3.rar"],         #
        #     "/path/to/folder2": ["file1.rar", "file2.rar", "file3.rar"]          #
        # }                                                                        #
        ############################################################################
        SimpleLogger.log.info_msg(f"Scanning root path '{self.root_path}' for folders containing archive files")

        # Generate archive_folders dictionary
        for root, dirs, files in os.walk(self.root_path):
            if not self.thread_active:
                SimpleLogger.log.info_msg("ArchiveScanner thread cancelled, aborting")
                return None

            for file in files:
                if not self.thread_active:
                    SimpleLogger.log.info_msg("ArchiveScanner thread cancelled, aborting")
                    return None

                if self.__is_archive_format_supported(file):
                    if root not in archive_folders:
                        archive_folders.update({root: [file]})
                    elif root in archive_folders:
                        archive_folders.get(root).append(file)
        SimpleLogger.log.info_msg(f"Found: {len(archive_folders)} folder(s) containing archive files")

        # Weed out potential split archives from archive_folders
        SimpleLogger.log.info_msg("Removing subsequent split archive files from file lists")
        for folder in archive_folders:
            if not self.thread_active:
                SimpleLogger.log.info_msg("ArchiveScanner thread cancelled, aborting")
                return None

            file_list = archive_folders.get(folder)
            if len(file_list) > 1:
                for file_name in file_list.copy():
                    if self.__is_partial_file(file_name):
                        file_list.remove(file_name)

        return archive_folders

    @staticmethod
    def __determine_archive_format(file_name):
        """Determines the archive format of the given file"""
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension in SUPPORTED_ARCHIVE_FORMATS:
            return file_extension

    @staticmethod
    def __is_archive_format_supported(file_name):
        """Checks to see if the given file is a supported archive format"""
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension in SUPPORTED_ARCHIVE_FORMATS:
            return True

        return False

    @staticmethod
    def __is_partial_file(file_name):
        """Determines if the file is part of a split archive"""
        for regex in PARTIAL_FILE_REGEX:
            match = re.match(regex, file_name)
            if match:
                part_number = int(match.group(2))
                if part_number != 1:
                    return True

        return False
