import win32com.client as win32

class App_Handler:
    def __init__(self):
        self.Word = win32.gencache.EnsureDispatch('Word.Application')
        self.Excel = win32.gencache.EnsureDispatch('Excel.Application')
        self.Power_Point = win32.gencache.EnsureDispatch('PowerPoint.Application')

    #make the excel Visible
    def open_excel(self):
        self.Excel.Visible = True

    #close every open excels
    def close_excel(self):
        self.Excel.Quit()

    # make the word Visible
    def open_word(self):
        self.Word.Visible = True

    # close every open word
    def close_word(self):
        self.Word.Quit()

    # make the power point Visible
    def open_power_point(self):
        self.Power_Point.Visible = True

    # close every open power point
    def close_power_point(self):
        self.Power_Point.Quit()

    #open the file and and made the application visible
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
