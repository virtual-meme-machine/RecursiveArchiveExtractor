import os
import wx

from lib import StringManager
from lib.gui import MainPanel

WINDOW_SIZE = wx.Size(805, 675)


class MainFrame(wx.Frame):
    """Main window for the application"""

    def __init__(self):
        """Initialize window parameters"""
        super().__init__(parent=None)

        # Set window properties
        self.SetTitle(StringManager.SM.window_title_main)
        self.SetIcon(wx.Icon(os.path.join("data", "icon.ico")))
        self.EnableMaximizeButton(False)
        self.SetMinSize(WINDOW_SIZE)
        self.SetMaxSize(WINDOW_SIZE)
        self.SetSize(WINDOW_SIZE)
        panel = MainPanel.MainPanel(self)

        # Set window to visible
        self.Show()
