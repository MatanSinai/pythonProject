import win32com.client as win32
import pandas as pd
from pathlib import Path


class ms_example:

    def __init__(self):
        self.application = None

    def open_excel(self):
        self.application = win32.gencache.EnsureDispatch('Excel.Application')
        self.application.Visible = True
        _ = input("Press ENTER to quit:")
        self.application.Application.Quit()

    def open_word(self):
        self.application = win32.gencache.EnsureDispatch('Word.Application')
        self.application.Visible = True
        _ = input("Press ENTER to quit:")
        self.application.Application.Quit()


    def open_pp(self):
        self.application = win32.gencache.EnsureDispatch('PowerPoint.Application')
        self.application.Visible = True
        _ = input("Press ENTER to quit:")
        self.application.Application.Quit()
