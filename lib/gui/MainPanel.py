import os
import wx

from lib import StringManager, ArchiveScanner, HumanBytes, ExtractionWorker

# Panel widget size variables
PADDING_AMOUNT = 5
SIZER_RATIO_TEXTBOX = 60
SIZER_RATIO_BUTTON = 10
SIZER_RATIO_PROGRESS_BAR = 100
SIZER_RATIO_PROGRESS_PERCENT = 5
FILE_LIST_BOX_SIZE = wx.Size(-1, 400)
FILE_LIST_FILE_NAME_COLUMN_WIDTH = 220
FILE_LIST_FILE_PATH_COLUMN_WIDTH = 400
FILE_LIST_ARCHIVE_FORMAT_COLUMN_WIDTH = 75
FILE_LIST_ARCHIVE_SIZE_COLUMN_WIDTH = 75
PROGRESS_BAR_SIZE = (0, 25)


class MainPanel(wx.Panel):
    """Window contents for main window of the application"""
    archive_file_list = []
    scan_in_progress = False
    extract_in_progress = False
    scan_thread = None
    extract_thread = None

    def __init__(self, parent):
        """Initialize panel widgets"""
        super().__init__(parent)

        # Create sizer objects that store UI widgets
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.container_sizer = wx.BoxSizer(wx.VERTICAL)

        # Init Root Path Selection Interface
        ############################################################################################################
        # Root path label
        self.root_path_label = wx.StaticText(self, label=StringManager.SM.section_label_root_path, style=wx.ALIGN_LEFT)
        self.container_sizer.Add(self.root_path_label, 0)
        # Root path text box
        self.root_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.root_path_entry_textbox = wx.TextCtrl(self)
        self.root_path_entry_textbox.AutoCompleteDirectories()
        self.root_path_sizer.Add(self.root_path_entry_textbox, SIZER_RATIO_TEXTBOX)
        # Root path browse button
        self.root_path_entry_browse_button = wx.Button(self, label=StringManager.SM.button_label_browse)
        self.root_path_entry_browse_button.Bind(wx.EVT_BUTTON, self.__button_browse_root_path)
        self.root_path_sizer.Add(self.root_path_entry_browse_button, SIZER_RATIO_BUTTON, wx.LEFT, PADDING_AMOUNT)
        # Root path scan button
        self.root_path_entry_scan_button = wx.Button(self, label=StringManager.SM.button_label_scan)
        self.root_path_entry_scan_button.Bind(wx.EVT_BUTTON, self.__button_scan_root_path)
        self.root_path_sizer.Add(self.root_path_entry_scan_button, SIZER_RATIO_BUTTON, wx.LEFT, PADDING_AMOUNT)
        self.container_sizer.Add(self.root_path_sizer, 0, wx.TOP | wx.EXPAND, PADDING_AMOUNT)
        # Divider line
        self.root_path_divide_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.container_sizer.Add(self.root_path_divide_line, 0, wx.TOP | wx.EXPAND, PADDING_AMOUNT * 2)
        ############################################################################################################

        # Init Archive File List Interface
        ############################################################################################################
        # Archive file list label
        self.file_list_label = wx.StaticText(self, label=StringManager.SM.section_label_file_list, style=wx.ALIGN_LEFT)
        self.container_sizer.Add(self.file_list_label, 0, wx.TOP, PADDING_AMOUNT)
        # Archive file list
        self.file_list_ctrl = wx.ListCtrl(self, size=FILE_LIST_BOX_SIZE, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.__init_file_list_columns()
        self.container_sizer.Add(self.file_list_ctrl, 0, wx.TOP | wx.EXPAND, PADDING_AMOUNT)
        # Archive file count text
        self.file_count_text = wx.StaticText(self, label=StringManager.SM.file_count_init_message, style=wx.ALIGN_LEFT)
        self.container_sizer.Add(self.file_count_text, 0, wx.TOP, PADDING_AMOUNT)
        # Divider line
        self.file_list_divide_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.container_sizer.Add(self.file_list_divide_line, 0, wx.TOP | wx.EXPAND, PADDING_AMOUNT)
        ############################################################################################################

        # Init Progress Bar Interface
        ############################################################################################################
        # Progress bar label
        self.progress_bar_label = wx.StaticText(self, label=StringManager.SM.section_label_progress_bar, style=wx.ALIGN_LEFT)
        self.container_sizer.Add(self.progress_bar_label, 0, wx.TOP, PADDING_AMOUNT)
        # Progress bar
        self.progress_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.extract_progress_bar = wx.Gauge(self, size=PROGRESS_BAR_SIZE, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.progress_bar_sizer.Add(self.extract_progress_bar, SIZER_RATIO_PROGRESS_BAR)
        # Progress status text
        self.progress_bar_percent_text = wx.StaticText(self, label=" ", style=wx.ALIGN_LEFT)
        self.progress_bar_sizer.Add(self.progress_bar_percent_text, SIZER_RATIO_PROGRESS_PERCENT, wx.CENTER)
        self.refresh_progress_bar(0, 0)
        self.container_sizer.Add(self.progress_bar_sizer, 0, wx.TOP | wx.EXPAND, PADDING_AMOUNT)
        # Divider line
        self.progress_bar_divide_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.container_sizer.Add(self.progress_bar_divide_line, 0, wx.TOP | wx.EXPAND, PADDING_AMOUNT * 2)
        ############################################################################################################

        # Init Extraction Path Selection Interface
        ############################################################################################################
        # Extract path label
        self.extract_path_label = wx.StaticText(self, label=StringManager.SM.section_label_extract_path, style=wx.ALIGN_LEFT)
        self.container_sizer.Add(self.extract_path_label, 0, wx.TOP, PADDING_AMOUNT)
        # Extract path text box
        self.extract_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.extract_path_entry_textbox = wx.TextCtrl(self)
        self.extract_path_entry_textbox.AutoCompleteDirectories()
        self.extract_path_sizer.Add(self.extract_path_entry_textbox, SIZER_RATIO_TEXTBOX)
        # Extract path browse button
        self.extract_path_entry_browse_button = wx.Button(self, label=StringManager.SM.button_label_browse)
        self.extract_path_entry_browse_button.Bind(wx.EVT_BUTTON, self.__button_browse_extract_path)
        self.extract_path_sizer.Add(self.extract_path_entry_browse_button, SIZER_RATIO_BUTTON, wx.LEFT, PADDING_AMOUNT)
        # Extract path extract all button
        self.extract_path_entry_scan_button = wx.Button(self, label=StringManager.SM.button_label_extract_all)
        self.extract_path_entry_scan_button.Bind(wx.EVT_BUTTON, self.__button_extract_all)
        self.extract_path_sizer.Add(self.extract_path_entry_scan_button, SIZER_RATIO_BUTTON, wx.LEFT, PADDING_AMOUNT)
        self.container_sizer.Add(self.extract_path_sizer, 0, wx.TOP | wx.EXPAND, PADDING_AMOUNT)
        ############################################################################################################

        # Add container_sizer into main_sizer and
        self.main_sizer.Add(self.container_sizer, 0, wx.ALL | wx.EXPAND, PADDING_AMOUNT * 1.5)
        self.SetSizer(self.main_sizer)

    def __button_browse_root_path(self, event):
        """Interface for setting the root path via a directory selection dialog window"""
        # Abort out if an operation is in progress
        if self.scan_in_progress or self.extract_in_progress:
            return

        # Create dialog window, set root_path_entry_textbox to path selected via dialog
        dlg = wx.DirDialog(self, StringManager.SM.window_title_browse_dialog, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            if os.path.isdir(dlg.GetPath()):
                self.root_path_entry_textbox.SetValue(dlg.GetPath())

        # If extract_path_entry_textbox is empty, set it to the selected path as well
        if self.extract_path_entry_textbox.GetValue() is None or self.extract_path_entry_textbox.GetValue() == "":
            if os.path.isdir(dlg.GetPath()):
                self.extract_path_entry_textbox.SetValue(dlg.GetPath())

        # Close dialog window thread and initiate scan of selected root path
        dlg.Destroy()
        self.__button_scan_root_path(event)

    def __button_browse_extract_path(self, event):
        """Interface for setting the extract path via a directory selection dialog window"""
        # Abort out if an operation is in progress
        if self.scan_in_progress or self.extract_in_progress:
            return

        # Create dialog window, set extract_path_entry_textbox to path selected via dialog
        dlg = wx.DirDialog(self, StringManager.SM.window_title_browse_dialog, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            if os.path.isdir(dlg.GetPath()):
                self.extract_path_entry_textbox.SetValue(dlg.GetPath())
        dlg.Destroy()

    def __button_scan_root_path(self, event):
        """Starts a thread that recursively scan the root path for archive files to add to 'archive_file_list'"""
        # Abort if extract is already in progress
        if self.extract_in_progress:
            return

        # If scan button was clicked while scan thread is still active, kill it to cancel the scan
        if self.scan_in_progress:
            if self.scan_thread.is_alive():
                self.scan_thread.thread_active = False
                self.scan_thread.join(timeout=10)
            while self.scan_thread.is_alive():
                print("fuck")
            self.archive_file_list.clear()
            self.refresh_file_list_contents()
            self.scan_in_progress = False
            return

        if self.scan_thread:
            return

        # Start archive scan thread in background
        self.scan_in_progress = True
        self.scan_thread = ArchiveScanner.ArchiveScanner(self)
        self.scan_thread.start()

    def __button_extract_all(self, event):
        """Starts a thread that extracts all archive files in 'archive_file_list' to the extract path"""
        # Abort out if an operation is in progress
        if self.scan_in_progress or self.extract_in_progress:
            return

        # Start extract thread in background
        self.extract_in_progress = True
        extract_thread = ExtractionWorker.ExtractionWorker(self)
        extract_thread.start()

    def __init_file_list_columns(self):
        """(Re)Initializes the the columns in the file list box"""
        col_0_size = FILE_LIST_FILE_NAME_COLUMN_WIDTH
        col_1_size = FILE_LIST_FILE_PATH_COLUMN_WIDTH
        col_2_size = FILE_LIST_ARCHIVE_FORMAT_COLUMN_WIDTH
        col_3_size = FILE_LIST_ARCHIVE_SIZE_COLUMN_WIDTH

        # If columns have already been initialized before, store their width so it can be restored
        if self.file_list_ctrl.GetColumnCount() > 0:
            col_0_size = self.file_list_ctrl.GetColumnWidth(0)
            col_1_size = self.file_list_ctrl.GetColumnWidth(1)
            col_2_size = self.file_list_ctrl.GetColumnWidth(2)
            col_3_size = self.file_list_ctrl.GetColumnWidth(3)

        # Clear columns then regenerate columns
        self.file_list_ctrl.ClearAll()
        self.file_list_ctrl.InsertColumn(0, StringManager.SM.file_list_file_name, width=col_0_size)
        self.file_list_ctrl.InsertColumn(1, StringManager.SM.file_list_file_path, width=col_1_size)
        self.file_list_ctrl.InsertColumn(2, StringManager.SM.file_list_archive_format, width=col_2_size)
        self.file_list_ctrl.InsertColumn(3, StringManager.SM.file_list_archive_size, width=col_3_size)

    def refresh_file_list_contents(self):
        """Refreshes the contents of the file list box based on the items in 'archive_file_list'"""
        # Reset file list and progress bar back to initialized states and refresh file count
        self.__init_file_list_columns()
        self.refresh_file_count()
        self.refresh_progress_bar(0, len(self.archive_file_list))

        # If archive_file_list is empty return without populating file list
        if self.archive_file_list is None or len(self.archive_file_list) == 0:
            return

        # Iterate over ArchiveObjects in archive_file_list to populate file list
        index = 0
        for archive_file in self.archive_file_list:
            self.file_list_ctrl.InsertItem(index, archive_file.file_name)
            self.file_list_ctrl.SetItem(index, 1, archive_file.file_path)
            self.file_list_ctrl.SetItem(index, 2, archive_file.archive_format)
            self.file_list_ctrl.SetItem(index, 3, HumanBytes.HumanBytes.format(archive_file.archive_size, metric=True))
            index += 1

    def refresh_file_count(self):
        """Refreshes the file count text to reflect the current number of files in 'archive_file_list'"""
        file_count = len(self.archive_file_list)
        file_count_string = StringManager.SM.file_count_string_plural

        # Set to singular variant of file count string if needed
        if file_count == 1:
            file_count_string = StringManager.SM.file_count_string_singular

        self.file_count_text.SetLabel(f"    {file_count} {file_count_string}")

    def refresh_progress_bar(self, progress_count, progress_range):
        """Sets the progress bar to the given values"""

        def calculate_progress_percentage(numerator, denominator):
            """Calculates the percentage of work that has been completed"""
            if denominator == 0:
                return 0
            return int(numerator * 100 / denominator)

        # Update progress bar value and range if needed
        if self.extract_progress_bar.GetValue() != progress_count:
            self.extract_progress_bar.SetValue(progress_count)
        if self.extract_progress_bar.GetRange() != progress_range:
            self.extract_progress_bar.SetRange(progress_range)

        # Update progress bar percentage label
        percentage = calculate_progress_percentage(progress_count, progress_range)
        self.progress_bar_percent_text.SetLabel(f"  {percentage}%")
