import wx

from lib import SimpleLogger, StringManager
from lib.gui import WindowFrame


if __name__ == "__main__":
    """Entry point into the program"""
    SimpleLogger.initialize_logger()
    StringManager.initialize_string_manager()
    app = wx.App()
    frame = WindowFrame.MainFrame()
    app.MainLoop()
