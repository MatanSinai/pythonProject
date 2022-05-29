import win32com.client as win32
from pathlib import Path


class App_Handler:
    def __init__(self):
        self.Word = win32.gencache.EnsureDispatch('Word.Application')
        self.Excel = win32.gencache.EnsureDispatch('Excel.Application')
        self.Power_Point = win32.gencache.EnsureDispatch('PowerPoint.Application')

    def open_excel(self):
        self.Excel.Visible = True

    def close_excel(self):
        self.Excel.Quit()


    def open_word(self):
        self.Word.Visible = True

    def close_word(self):
        self.Word.Quit()


    def open_power_point(self):
        self.Power_Point.Visible = True

    def close_power_point(self):
        self.Power_Point.Quit()

    def open_file(self, file):
        if file.split(".")[-1] == 'xlsx':
            self.open_excel()
            self.Excel.Workbooks.Open(file)

        elif file.split(".")[-1] == 'docx':
            self.open_word()
            self.Word.Documents.Open(file)

        elif file.split(".")[-1] == 'pptx':
            self.open_power_point()
            self.Power_Point.Presentations.Open(file)
