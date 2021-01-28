import os
import sys
import wx

from lib import SimpleLogger, StringManager
from lib.gui import WindowFrame


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    Source: https://stackoverflow.com/a/13790741
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    """Entry point into the program"""
    data_dir = get_resource_path("data")
    SimpleLogger.initialize_logger()
    StringManager.initialize_string_manager(data_dir)
    app = wx.App()
    frame = WindowFrame.MainFrame(data_dir)
    app.MainLoop()
